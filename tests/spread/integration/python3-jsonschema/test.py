#!/usr/bin/env python3
"""Smoke test for python3-jsonschema package."""

import jsonschema

# Test basic JSON schema validation
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"}
    }
}

# Valid instance
instance = {"name": "Test"}
jsonschema.validate(instance, schema)

print("jsonschema smoke test passed")
