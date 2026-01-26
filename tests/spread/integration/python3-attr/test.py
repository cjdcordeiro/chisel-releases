#!/usr/bin/env python3
"""Smoke test for python3-attr package."""

import attr

# Test basic attr functionality
@attr.s
class Person:
    name = attr.ib()
    age = attr.ib()

# Create an instance
person = Person(name="Test", age=25)

# Verify attributes work
assert person.name == "Test"
assert person.age == 25

print("attr smoke test passed")
