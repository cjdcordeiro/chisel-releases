#!/usr/bin/env python3
"""Smoke test for python3-requests package."""

import requests

# Test that we can create a Session and access basic attributes
session = requests.Session()

# Verify session was created
assert session is not None
assert hasattr(session, 'headers')
assert hasattr(session, 'get')

print("requests smoke test passed")
