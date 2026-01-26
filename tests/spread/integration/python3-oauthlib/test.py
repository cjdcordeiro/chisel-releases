#!/usr/bin/env python3
"""Smoke test for python3-oauthlib package."""

from oauthlib.oauth2 import BackendApplicationClient

# Test basic OAuth2 client creation
client_id = "test_client_id"
client = BackendApplicationClient(client_id=client_id)

# Verify client was created
assert client.client_id == client_id

print("oauthlib smoke test passed")
