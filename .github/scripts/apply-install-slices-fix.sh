#!/bin/bash
# Script to apply the install-slices retry mechanism fix to all Ubuntu release branches
# Usage: ./apply-install-slices-fix.sh

set -e

BRANCHES=("ubuntu-20.04" "ubuntu-22.04" "ubuntu-24.04" "ubuntu-24.10" "ubuntu-25.04" "ubuntu-25.10")
FIX_FILE="tests/spread/lib/install-slices"

echo "This script will apply the install-slices retry mechanism fix to all Ubuntu release branches"
echo "Branches to update: ${BRANCHES[@]}"
echo ""

for branch in "${BRANCHES[@]}"; do
    echo "===================================="
    echo "Processing branch: $branch"
    echo "===================================="
    
    # Check if branch exists
    if ! git show-ref --verify --quiet "refs/remotes/origin/$branch"; then
        echo "Warning: Branch origin/$branch does not exist, skipping..."
        continue
    fi
    
    # Check if the file exists on this branch
    if ! git cat-file -e "origin/$branch:$FIX_FILE" 2>/dev/null; then
        echo "Warning: File $FIX_FILE does not exist on branch $branch, skipping..."
        continue
    fi
    
    # Create a new branch for the fix
    fix_branch="${branch}-install-slices-retry-fix"
    echo "Creating branch: $fix_branch"
    
    git checkout -b "$fix_branch" "origin/$branch" || {
        echo "Branch already exists, checking out..."
        git checkout "$fix_branch"
    }
    
    # Apply the fix by replacing the file content
    cat > "$FIX_FILE" << 'EOF'
#!/bin/bash -ex

# Installs one or more slices into a dynamically created temporary path.
# Usage: install-slices [<slice>...]
# Returns the path of the chiselled rootfs

tmpdir="$(mktemp -d)"
echo "${tmpdir}"

max_attempts=3
attempt=1
fetch_error="error: cannot fetch from archive"

while [ $attempt -le $max_attempts ]; do
    output=$(chisel cut --release "$PROJECT_PATH" --root "$tmpdir" "$@" 2>&1)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        exit 0
    fi
    
    # Check if it's a fetch error that we should retry
    if echo "$output" | grep -q "$fetch_error"; then
        if [ $attempt -lt $max_attempts ]; then
            echo "Fetch error on attempt $attempt/$max_attempts, retrying..." >&2
            ((attempt++))
            continue
        fi
    fi
    
    # If we get here, either it's not a fetch error or we're out of retries
    echo "$output" >&2
    exit $exit_code
done
EOF
    
    # Ensure file is executable
    chmod +x "$FIX_FILE"
    
    # Check if there are changes
    if git diff --quiet "$FIX_FILE"; then
        echo "No changes needed for $branch"
    else
        echo "Changes detected, committing..."
        git add "$FIX_FILE"
        git commit -m "ci: add retry mechanism to install-slices helper in spread tests

This adds a retry mechanism (up to 3 attempts) to handle transient
'error: cannot fetch from archive' failures that occur when Ubuntu
archives are updated during test runs.

The fix matches the behavior already implemented in the Python CI
script in PR #721.

Fixes: #743"
        
        echo "Branch $fix_branch is ready to push"
        echo "To push: git push origin $fix_branch"
    fi
    
    echo ""
done

echo "===================================="
echo "Fix application complete!"
echo "===================================="
echo ""
echo "Next steps:"
echo "1. Review the changes in each branch"
echo "2. Push the branches: for branch in ${BRANCHES[@]}; do git push origin \${branch}-install-slices-retry-fix; done"
echo "3. Create pull requests for each branch to merge the fixes"
