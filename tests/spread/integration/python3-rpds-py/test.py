#!/usr/bin/env python3
"""Smoke test for python3-rpds-py package."""

import rpds

# Test persistent list
plist = rpds.List([1, 2, 3])
plist2 = plist.push_front(0)

# Verify immutability and operations
assert len(plist) == 3
assert len(plist2) == 4

print("rpds smoke test passed")
