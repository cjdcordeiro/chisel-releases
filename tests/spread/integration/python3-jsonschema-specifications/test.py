#!/usr/bin/env python3
"""Smoke test for python3-jsonschema-specifications package."""

import jsonschema_specifications

# Test that we can access specifications
specs = jsonschema_specifications.REGISTRY

# Verify registry exists and has content
assert specs is not None

print("jsonschema_specifications smoke test passed")
