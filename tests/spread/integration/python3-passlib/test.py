#!/usr/bin/env python3
"""Smoke test for python3-passlib package."""

from passlib.hash import sha256_crypt

# Test password hashing
password = "test_password"
hashed = sha256_crypt.hash(password)

# Verify hashing and verification work
assert sha256_crypt.verify(password, hashed)
assert not sha256_crypt.verify("wrong_password", hashed)

print("passlib smoke test passed")
