#!/usr/bin/env python3
"""Smoke test for python3-markupsafe package."""

from markupsafe import escape

# Test HTML escaping
unsafe_html = "<script>alert('xss')</script>"
safe_html = escape(unsafe_html)

# Verify escaping works
assert "&lt;script&gt;" in str(safe_html)
assert "<script>" not in str(safe_html)

print("markupsafe smoke test passed")
