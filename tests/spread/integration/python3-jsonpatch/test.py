#!/usr/bin/env python3
"""Smoke test for python3-jsonpatch package."""

import jsonpatch

# Test JSON patch functionality
doc = {"foo": "bar"}
patch = [{"op": "add", "path": "/baz", "value": "qux"}]
result = jsonpatch.apply_patch(doc, patch)

# Verify patch application works
assert result["baz"] == "qux"
assert result["foo"] == "bar"

print("jsonpatch smoke test passed")
