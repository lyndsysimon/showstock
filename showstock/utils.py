"""
Utility functions and classes for the Showstock application.
"""

from typing import Any, Dict, Type


class SingletonMeta(type):
    """
    Metaclass for implementing the Singleton pattern.

    Classes that use this metaclass will only ever have one instance.
    Subsequent calls to the class constructor will return the same instance.

    Example:
        ```python
        class MyClass(metaclass=SingletonMeta):
            pass

        a = MyClass()
        b = MyClass()
        assert a is b  # True
        ```
    """

    _instances: Dict[Type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """
        Override the call behavior to implement the singleton pattern.

        Args:
            *args: Arguments to pass to the class constructor
            **kwargs: Keyword arguments to pass to the class constructor

        Returns:
            The singleton instance of the class
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
