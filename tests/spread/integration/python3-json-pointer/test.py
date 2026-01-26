#!/usr/bin/env python3
"""Smoke test for python3-json-pointer package."""

import jsonpointer

# Test JSON pointer functionality
doc = {"foo": {"bar": "baz"}}
pointer = jsonpointer.JsonPointer("/foo/bar")
value = pointer.resolve(doc)

# Verify pointer resolution works
assert value == "baz"

print("jsonpointer smoke test passed")
