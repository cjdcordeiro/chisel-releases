#!/usr/bin/env python3
"""Smoke test for python3-certifi package."""

import certifi

# Test that we can get the CA bundle path
ca_bundle = certifi.where()

# Verify it returns a path
assert isinstance(ca_bundle, str)
assert len(ca_bundle) > 0

print("certifi smoke test passed")
