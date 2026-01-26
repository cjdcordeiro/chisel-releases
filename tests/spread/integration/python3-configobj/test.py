#!/usr/bin/env python3
"""Smoke test for python3-configobj package."""

from configobj import ConfigObj

# Test basic ConfigObj functionality
config = ConfigObj()
config['section1'] = {}
config['section1']['key1'] = 'value1'

# Verify values
assert config['section1']['key1'] == 'value1'

print("configobj smoke test passed")
