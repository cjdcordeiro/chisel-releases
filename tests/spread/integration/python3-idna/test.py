#!/usr/bin/env python3
"""Smoke test for python3-idna package."""

import idna

# Test IDNA encoding/decoding
domain = "example.com"
encoded = idna.encode(domain)
decoded = idna.decode(encoded)

# Verify round-trip works
assert decoded == domain

print("idna smoke test passed")
