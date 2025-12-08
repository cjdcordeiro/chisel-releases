# Copilot Instructions: Slices and Tests CI

This document describes the CI tests that are executed when a Pull Request is raised against any `ubuntu-*` branch in the chisel-releases repository, specifically focusing on the `slices/` and `tests/` folders.

## Overview

When contributing to chisel-releases, all PRs targeting `ubuntu-*` branches (e.g., `ubuntu-22.04`, `ubuntu-24.04`, `ubuntu-25.04`) trigger multiple CI workflows that validate slice definitions and run integration tests. Understanding these tests helps ensure your contributions pass CI on the first attempt.

## Key CI Workflows for Slices and Tests

### 1. **Install Slices** (`install-slices.yaml`)

**Purpose**: Validates that slices can be successfully installed using Chisel.

**Triggers**: 
- Pull requests to any branch
- Changes to slice definition files (`slices/**/*.yaml`)
- Changes to `chisel.yaml`

**What it tests**:
- **Selective testing**: Installs only slices from **added** or **modified** slice definition files
- **Full testing**: Installs **all** slices if:
  - `chisel.yaml` is changed
  - Any slice definition files are deleted
  - Workflow files are modified

**Test matrix**:
- Multiple architectures: `amd64`, `arm64`, `armhf`, `ppc64el`, `riscv64`, `s390x`
- Multiple Chisel versions for compatibility (e.g., `v1.1.0`, `v1.2.0`, `main`)
- Tests the specific `ubuntu-*` branch being modified

**What to ensure**:
- Slices install without errors across all supported architectures
- Package dependencies are correctly specified
- File paths in slice definitions are valid
- Content mutations work as expected

---

### 2. **Spread Tests** (`spread.yaml`)

**Purpose**: Runs integration tests for slices using the Spread testing framework.

**Triggers**:
- Pull requests to any branch
- Changes to slice files (`slices/**/*.yaml`)
- Changes to test directories (`tests/spread/integration/**`)

**What it tests**:
- Package-specific integration tests located in `tests/spread/integration/<package-name>/`
- Tests run only for:
  - Packages with **modified** or **added** slice definitions
  - Test directories that have changed

**Test matrix**:
- Runs on both X64 and ARM64 runners
- Uses LXD backend for isolated testing environments

**How it works**:
1. Detects changed slice files (e.g., `slices/base-files.yaml`)
2. Looks for corresponding test directory (e.g., `tests/spread/integration/base-files/`)
3. Executes `task.yaml` in that directory if it exists
4. Each test runs in an isolated LXD container

**What to ensure**:
- If you add/modify a slice, consider adding integration tests in `tests/spread/integration/<pkg-name>/task.yaml`
- Tests should verify the slice installs correctly and provides expected functionality
- Tests are idempotent and clean up after themselves

---

### 3. **Lint** (`lint.yaml`)

**Purpose**: Validates YAML syntax and enforces slice definition conventions.

**Triggers**:
- Pull requests to any branch
- Changes to slice files

**What it checks**:

**a) YAML Syntax (yamllint)**:
- Proper YAML formatting
- Correct indentation
- Valid structure
- Configuration in `.github/yamllint.yaml`

**b) SDF-Specific Rules**:
- **Sorted `essential` entries**: All entries in a slice's `essential` field must be alphabetically sorted
  ```yaml
  slices:
    libs:
      essential:
        - base-files_libs  # Must be sorted
        - libc6_libs
  ```
- **Sorted `contents` keys**: All keys in a slice's `contents` field must be alphabetically sorted
  ```yaml
  slices:
    bins:
      contents:
        /usr/bin/foo: {}
        /usr/bin/bar: {}  # Keys must be sorted alphabetically
  ```

**What to ensure**:
- Run `yamllint` locally before submitting
- Ensure `essential` and `contents` entries are alphabetically sorted
- Use consistent formatting throughout slice definitions

---

### 4. **Package Dependencies** (`pkg-deps.yaml`)

**Purpose**: Analyzes and reports on package dependencies for modified slices.

**Triggers**:
- Pull requests to `ubuntu-*` branches
- Changes to slice definition files (`slices/**/*.yaml`)

**What it does**:
- Checks dependencies for modified slices
- Posts informational messages to the PR with dependency analysis
- Helps reviewers understand the impact of slice changes

**What to ensure**:
- Review the dependency report posted to your PR
- Verify that dependencies are intentional and correct
- Ensure no circular dependencies are introduced

---

### 5. **Removed Slices** (`removed-slices.yaml`)

**Purpose**: Detects and validates when slices are removed from slice definitions.

**Triggers**:
- Pull requests that modify files in `slices/`

**What it checks**:
- Identifies any slices that have been removed
- Ensures removals are intentional and documented
- Prevents accidental deletion of slices

**What to ensure**:
- Document why slices are being removed in your PR description
- Consider deprecation path if slices are widely used
- Update any tests that reference removed slices

---

## Branch-Specific Behavior

### PRs to `ubuntu-*` branches (e.g., ubuntu-24.04)
- **Focused testing**: Only tests the specific branch being modified
- **Changed files only**: Tests run only for modified/added slices
- Uses compatible Chisel versions for that release

### PRs to `main` branch
- **Comprehensive testing**: Tests all `ubuntu-*` branches
- **Full validation**: Installs all slices across all maintained releases
- More extensive CI time required

---

## Best Practices for Contributors

### When modifying slices:

1. **Lint locally first**:
   ```bash
   yamllint -c .github/yamllint.yaml slices/
   ```

2. **Sort entries**: Ensure `essential` and `contents` are alphabetically sorted

3. **Add tests**: If adding new slices, create integration tests in `tests/spread/integration/<pkg-name>/`

4. **Test installation locally**:
   ```bash
   chisel cut --release ./ --root /tmp/rootfs package_slice
   ```

5. **Check all architectures**: Consider how your changes affect different architectures

### When writing tests:

1. **Location**: Place tests in `tests/spread/integration/<package-name>/task.yaml`

2. **Scope**: Test the actual functionality the slice provides, not just installation

3. **Isolation**: Tests should not depend on external state or other tests

4. **Cleanup**: Ensure tests clean up any resources they create

5. **Documentation**: Add comments explaining what the test validates

---

## Common CI Failures and Solutions

### Lint failures (sorting)
**Error**: `"essential" entries are not sorted`
**Solution**: Sort the `essential` array alphabetically:
```yaml
essential:
  - base-files_libs
  - libc6_libs
  - zlib1g_libs
```

### Install failures
**Error**: `cannot install slice: package not found`
**Solution**: 
- Verify package exists in the Ubuntu archive for that release
- Check the archive URL in `chisel.yaml`
- Ensure package name is spelled correctly

### Spread test failures
**Error**: `task.yaml not found`
**Solution**: If you modified a slice, ensure corresponding tests exist or are updated

### Architecture-specific failures
**Error**: Tests pass on amd64 but fail on arm64
**Solution**: 
- Check for architecture-specific paths or binaries
- Verify the package is available for that architecture
- Test using `chisel cut --arch arm64`

---

## Workflow Diagram

```
PR Opened → ubuntu-* branch
    ↓
    ├─→ Lint (yamllint + SDF rules)
    ├─→ Install Slices (changed slices, multiple arches)
    ├─→ Spread Tests (integration tests for changed pkgs)
    ├─→ Package Dependencies (dependency analysis)
    └─→ Removed Slices Check (if slices deleted)
    ↓
All checks pass ✓ → Ready for review
```

---

## Additional Resources

- [Chisel Documentation](https://documentation.ubuntu.com/chisel/en/latest/)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Spread Testing Framework](https://github.com/snapcore/spread)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## Quick Reference

| Workflow | Triggers On | What it Tests | Scope |
|----------|-------------|---------------|-------|
| install-slices | Slice changes | Installation across arches | Changed slices only (or all if chisel.yaml modified) |
| spread | Slice/test changes | Integration tests | Changed packages only |
| lint | Slice changes | YAML syntax + SDF rules | All modified files |
| pkg-deps | Slice changes | Dependencies | Changed slices only |
| removed-slices | Slice deletions | Removal validation | Deleted slices |

---

*Last updated: December 8, 2025*
