# AppConfig Usage Guide

The `AppConfig` class is a singleton that represents the web application's configuration. It provides a centralized place to store and access configuration values that are used throughout the application.

## Basic Usage

```python
from showstock.config import app_config

# Get the current salt value
current_salt = app_config.salt

# Set a new salt value
app_config.salt = "new-salt-value"
```

## Singleton Behavior

The `AppConfig` class is implemented as a singleton using the `SingletonMeta` metaclass from `showstock.utils`. This ensures that only one instance of the class exists throughout the application, so all parts of the application are using the same configuration values.

```python
from showstock.config import AppConfig, app_config

# These are all the same instance
config1 = AppConfig()
config2 = AppConfig()
config3 = app_config

assert config1 is config2
assert config2 is config3
```

## Configuration Values

Currently, the `AppConfig` class has the following configuration values:

- `salt`: A secret value used for creating and validating hashes.

## Implementation Details

The `AppConfig` class uses the `SingletonMeta` metaclass to implement the singleton pattern in a Pythonic way:

```python
from showstock.utils import SingletonMeta

class AppConfig(metaclass=SingletonMeta):
    def __init__(self):
        self.salt = "default-salt-value-change-in-production"
```

This approach has several advantages:
1. It's more Pythonic than overriding `__new__`
2. It separates the singleton logic from the class implementation
3. It can be reused for other singleton classes in the application

The class uses direct attribute access for simplicity. If future requirements demand more complex behavior (such as validation, side effects, or computed values), the implementation can be enhanced with property decorators without changing the interface.

## Integration with Settings

The `AppConfig` class is separate from the `Settings` class, which is used for loading configuration from environment variables. In the future, these two classes could be integrated to provide a more unified configuration system.
