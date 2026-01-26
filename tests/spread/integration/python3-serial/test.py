#!/usr/bin/env python3
"""Smoke test for python3-serial package."""

import serial

# Test basic serial module functionality
# Just verify we can access key classes
assert hasattr(serial, 'Serial')
assert hasattr(serial, 'SerialException')

print("serial smoke test passed")
