"""
Tests for the configuration module.
"""

from showstock.config import AppConfig


def test_app_config_singleton():
    """Test that AppConfig is a singleton."""
    config1 = AppConfig()
    config2 = AppConfig()
    
    # Both instances should be the same object
    assert config1 is config2
    
    # Changing an attribute on one instance should affect the other
    config1.salt = "new-salt-value"
    assert config2.salt == "new-salt-value"
    
    # Reset to default for other tests
    config1.salt = "default-salt-value-change-in-production"


def test_app_config_salt():
    """Test that the salt attribute works correctly."""
    config = AppConfig()
    
    # Test default value
    assert config.salt == "default-salt-value-change-in-production"
    
    # Test setting a new value
    config.salt = "test-salt"
    assert config.salt == "test-salt"
    
    # Reset to default for other tests
    config.salt = "default-salt-value-change-in-production"