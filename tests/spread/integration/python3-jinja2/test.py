#!/usr/bin/env python3
"""Smoke test for python3-jinja2 package."""

from jinja2 import Template

# Test basic template rendering
template = Template("Hello {{ name }}!")
result = template.render(name="World")

# Verify rendering works
assert result == "Hello World!"

print("jinja2 smoke test passed")
