---
applyTo: "slices/*,tests/spread/integration/**"
---

When reviewing code, consider any of these files as Slice Definitions Files (aka SDF), and focus on:

## The existence of the SDF in higher ubuntu-* branches
- Ensure the SDF exist in higher ubuntu-* branches (e.g. if reviewing a PR for ubuntu-24.04, check if the SDF exists for ubuntu-24.10 and newer branches)
- If the SDF does not exist in higher branches, check if there is an open PR proposing it

## Slice Definition File content
- There must be a "copyright" slice at the bottom of the SDF
- If there are any "content" paths in the SDF that are either scripts or binaries, then there must be a corresponding folder in tests/spread/integration/ with the same package name

## Validate the code quality of the tests
- Each test folder (under tests/spread/integration/) should have one task.yaml file where the "execute" field is a bash script that needs to be reviewed
- Inside the same tests folder, there may be other scripts, in various languages, that also need to be reviewed
