# Install-Slices Retry Fix Patches

This directory contains patch files for applying the install-slices retry mechanism fix to all Ubuntu release branches.

## What's in the Patches

Each patch file adds a retry mechanism to `tests/spread/lib/install-slices` that:
- Retries up to 3 times on "error: cannot fetch from archive" failures
- Logs retry attempts to stderr
- Maintains backward compatibility
- Matches the behavior from PR #721 (Python CI script)

## Available Patches

- `ubuntu-20.04.patch` - For ubuntu-20.04 branch
- `ubuntu-22.04.patch` - For ubuntu-22.04 branch
- `ubuntu-24.04.patch` - For ubuntu-24.04 branch
- `ubuntu-24.10.patch` - For ubuntu-24.10 branch
- `ubuntu-25.04.patch` - For ubuntu-25.04 branch
- `ubuntu-25.10.patch` - For ubuntu-25.10 branch

## How to Apply

### Option 1: Apply to All Branches

```bash
#!/bin/bash
BRANCHES=("ubuntu-20.04" "ubuntu-22.04" "ubuntu-24.04" "ubuntu-24.10" "ubuntu-25.04" "ubuntu-25.10")

for branch in "${BRANCHES[@]}"; do
    echo "Applying patch to $branch..."
    git checkout "$branch"
    git apply "patches/install-slices-retry-fix/${branch}.patch"
    git add tests/spread/lib/install-slices
    git commit -m "ci: add retry mechanism to install-slices helper in spread tests"
done
```

### Option 2: Apply to a Single Branch

```bash
# Example for ubuntu-24.04
git checkout ubuntu-24.04
git apply patches/install-slices-retry-fix/ubuntu-24.04.patch
git add tests/spread/lib/install-slices
git commit -m "ci: add retry mechanism to install-slices helper in spread tests"
```

### Option 3: Use git am (includes commit message)

```bash
# Example for ubuntu-24.04
git checkout ubuntu-24.04
git am patches/install-slices-retry-fix/ubuntu-24.04.patch
```

## Verification

After applying a patch, verify it was applied correctly:

```bash
# Check the file was modified
git diff HEAD~1 tests/spread/lib/install-slices

# View the updated file
cat tests/spread/lib/install-slices
```

The updated file should contain:
- A `max_attempts=3` variable
- A `while` loop for retries
- Error detection logic for "error: cannot fetch from archive"
- Retry logging to stderr

## Testing

The fix maintains backward compatibility:
- Same script interface
- Same behavior for successful runs
- Only adds retry logic for the specific archive fetch error

## References

- Issue: #743
- Related PR (Python CI): #721
- Full documentation: See `INSTALL_SLICES_FIX.md` in the repository root
