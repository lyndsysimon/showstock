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

The `AppConfig` class is implemented as a singleton, which means that only one instance of the class exists throughout the application. This ensures that all parts of the application are using the same configuration values.

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

## Simple Implementation

The `AppConfig` class uses a straightforward implementation with direct attribute access. This approach was chosen for simplicity since the current requirements don't need advanced features like validation or computed values.

If future requirements demand more complex behavior (such as validation, side effects, or computed values), the implementation can be enhanced with property decorators without changing the interface.

## Integration with Settings

The `AppConfig` class is separate from the `Settings` class, which is used for loading configuration from environment variables. In the future, these two classes could be integrated to provide a more unified configuration system.