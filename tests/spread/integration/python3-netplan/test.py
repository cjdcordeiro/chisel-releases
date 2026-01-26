#!/usr/bin/env python3
"""Smoke test for python3-netplan package."""

import netplan

# Test basic netplan module import and API availability
# Just verify we can access the Parser class
assert hasattr(netplan, 'Parser')

print("netplan smoke test passed")
