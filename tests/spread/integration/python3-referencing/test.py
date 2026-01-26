#!/usr/bin/env python3
"""Smoke test for python3-referencing package."""

import referencing
from referencing import Resource
from referencing.jsonschema import DRAFT7

# Test basic referencing functionality with explicit specification
resource = Resource(contents={"type": "object"}, specification=DRAFT7)

# Verify resource was created
assert resource is not None
assert resource.contents["type"] == "object"

print("referencing smoke test passed")
