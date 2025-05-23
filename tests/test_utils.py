"""
Tests for the utils module.
"""

from showstock.utils import SingletonMeta


def test_singleton_meta():
    """Test that SingletonMeta creates singleton classes."""

    # Create a test class using SingletonMeta
    class TestSingleton(metaclass=SingletonMeta):
        def __init__(self, value=None):
            self.value = value or "default"

    # Create two instances
    instance1 = TestSingleton("first")
    instance2 = TestSingleton("second")  # This should be ignored

    # Both instances should be the same object
    assert instance1 is instance2

    # The value should be from the first initialization
    assert instance1.value == "first"
    assert instance2.value == "first"  # Not "second"

    # Changing an attribute on one instance should affect the other
    instance1.value = "changed"
    assert instance2.value == "changed"
