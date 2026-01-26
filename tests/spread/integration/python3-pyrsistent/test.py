#!/usr/bin/env python3
"""Smoke test for python3-pyrsistent package."""

from pyrsistent import pvector

# Test persistent vector
v1 = pvector([1, 2, 3])
v2 = v1.append(4)

# Verify immutability and operations
assert len(v1) == 3
assert len(v2) == 4
assert v2[-1] == 4

print("pyrsistent smoke test passed")
