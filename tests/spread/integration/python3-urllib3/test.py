#!/usr/bin/env python3
"""Smoke test for python3-urllib3 package."""

import urllib3

# Test that we can create a PoolManager
pm = urllib3.PoolManager()

# Verify PoolManager was created
assert pm is not None
assert hasattr(pm, 'request')

print("urllib3 smoke test passed")
