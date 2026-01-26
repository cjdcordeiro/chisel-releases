#!/usr/bin/env python3
"""Smoke test for python3-typing-extensions package."""

from typing_extensions import Literal, TypedDict

# Test that we can use typing extensions
class Person(TypedDict):
    name: str
    age: int

# Test Literal type
def get_status() -> Literal["active", "inactive"]:
    return "active"

# Verify types are available
person: Person = {"name": "Test", "age": 25}
status = get_status()

assert person["name"] == "Test"
assert status == "active"

print("typing_extensions smoke test passed")
