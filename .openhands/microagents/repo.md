# Showstock Repository Information

## Code Style

- **Black**: Always run Black on Python files before committing changes
  ```bash
  black showstock/ tests/
  ```

## Repository Structure

- `showstock/`: Main application package
  - `config.py`: Contains the `AppConfig` singleton class for application configuration
- `tests/`: Test directory
  - `test_config.py`: Tests for the configuration system
- `docs/`: Documentation
  - `app_config_usage.md`: Documentation for using the AppConfig class
- `docker/`: Docker configuration
  - `Dockerfile`: Main application Dockerfile
  - `Dockerfile.tests`: Dockerfile for running tests
  - `compose.yaml`: Docker Compose configuration

## Testing

- Tests should only be run using Docker:
  ```bash
  docker compose -f docker/compose.yaml up tests
  ```

## Configuration

- Application configuration is managed through the `AppConfig` singleton class
- Access the global configuration instance via `from showstock.config import app_config`