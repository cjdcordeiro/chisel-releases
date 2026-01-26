#!/usr/bin/env python3
"""Smoke test for python3-yaml package."""

import yaml

# Test YAML parsing and dumping
data = {"name": "Test", "value": 42}
yaml_str = yaml.dump(data)
parsed = yaml.safe_load(yaml_str)

# Verify round-trip works
assert parsed["name"] == "Test"
assert parsed["value"] == 42

print("yaml smoke test passed")
