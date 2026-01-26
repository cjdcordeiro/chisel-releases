#!/usr/bin/env python3
"""Smoke test for python3-chardet package."""

import chardet

# Test character encoding detection
test_string = b"Hello, World!"
result = chardet.detect(test_string)

# Verify it returns a dict with expected keys
assert isinstance(result, dict)
assert 'encoding' in result
assert 'confidence' in result

print("chardet smoke test passed")
