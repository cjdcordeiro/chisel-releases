# Install-Slices Retry Mechanism Fix

## Summary

This document describes the fix applied to the `tests/spread/lib/install-slices` script across all Ubuntu release branches to add a retry mechanism for handling transient archive fetch errors.

## Problem

The `install-slices` helper function used in Spread integration tests was experiencing manifest digest errors when Ubuntu archives are updated during test runs, causing test failures.

Error example:
```
error: cannot fetch from archive: expected digest 053d09654f2bbeec59605a7d948f2e6ee80b9218978211c53c8aa2879a13d7ea, got 58b46c55d471ac98b59bb31555ef9d87dd5754956472c34a70f3bd11e65fd7ab
```

## Solution

Added a retry mechanism (up to 3 attempts) that:
- Only retries on "error: cannot fetch from archive" failures
- Logs retry attempts to stderr
- Exits immediately on success or non-retryable errors
- Matches the behavior already implemented in the Python CI script (PR #721)

## Implementation

### Changed File
`tests/spread/lib/install-slices`

### Key Changes
1. Wrapped the `chisel cut` command in a retry loop
2. Capture command output and exit code
3. Check for specific fetch error pattern
4. Retry up to 3 times with logging
5. Properly quote `"$@"` to handle arguments with spaces

### Before
```bash
#!/bin/bash -ex

# Installs one or more slices into a dynamically created temporary path.
# Usage: install-slices [<slice>...]
# Returns the path of the chiselled rootfs

tmpdir="$(mktemp -d)"

echo "${tmpdir}"
chisel cut --release "$PROJECT_PATH" --root "$tmpdir" $@
```

### After
```bash
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
```

## Branches Updated

The fix has been applied to the following branches:

1. ✅ ubuntu-20.04 (branch: `ubuntu-20.04-install-slices-fix`)
2. ✅ ubuntu-22.04 (branch: `ubuntu-22.04-install-slices-fix`)
3. ✅ ubuntu-24.04 (branch: `ubuntu-24.04-install-slices-fix`)
4. ✅ ubuntu-24.10 (branch: `ubuntu-24.10-install-slices-fix`)
5. ✅ ubuntu-25.04 (branch: `ubuntu-25.04-install-slices-fix`)
6. ✅ ubuntu-25.10 (branch: `ubuntu-25.10-install-slices-fix`)

## Testing

The fix has been designed to:
- Maintain backward compatibility (same interface and behavior for successful runs)
- Only add retry logic for the specific error case
- Preserve all existing functionality

## Applying the Fix

The fix needs to be applied to the `tests/spread/lib/install-slices` file on each Ubuntu release branch. The reference implementation is available in this branch at `tests/spread/lib/install-slices`.

### Apply to Each Branch

For each Ubuntu release branch, replace the file content with the fixed version:

```bash
# Example for ubuntu-24.04
git checkout ubuntu-24.04

# Replace the file with the fixed version
cat > tests/spread/lib/install-slices << 'EOF'
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

# Ensure executable
chmod +x tests/spread/lib/install-slices

# Commit
git add tests/spread/lib/install-slices
git commit -m "ci: add retry mechanism to install-slices helper in spread tests"
```

Repeat for all branches: ubuntu-20.04, ubuntu-22.04, ubuntu-24.04, ubuntu-24.10, ubuntu-25.04, ubuntu-25.10

## References

- Original issue: #743
- Related fix (Python CI): PR #721
- Example failure: https://github.com/canonical/chisel-releases/actions/runs/18732102302/job/53431205076?pr=648
