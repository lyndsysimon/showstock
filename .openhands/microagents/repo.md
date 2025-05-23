# Showstock Repository Information

## Project Overview

ShowStock is a web backend application that will:
- Support mobile and web frontends
- Help livestock owners manage nutrition for show animals
- Provide tools for developing and implementing feeding plans
- Track nutritional data and animal performance

## Code Style

- **Black**: Always run Black on Python files before committing changes
  ```bash
  black showstock/ tests/
  ```
- Use type hints throughout the codebase

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
- Write tests for all new functionality
- Write comprehensive tests for async code

## Configuration

- Application configuration is managed through the `AppConfig` singleton class
- Access the global configuration instance via `from showstock.config import app_config`

## Technical Rules and Guidelines

### Asynchronous Python Development
- All code must be written using asynchronous Python patterns
- Dependencies must support fully asynchronous use
- Only async code should be called when serving web requests
- Use `async`/`await` syntax consistently throughout the codebase
- Avoid blocking operations in request handlers
- Implement proper error handling for async code

### Containerization Requirements
- The project must be entirely containerized
- Never create Python environments directly on the host
- All commands must be run inside the appropriate container
- Use Docker for containerization
- Use Docker Compose for container orchestration
- Container configurations should be version controlled
- Follow container security best practices

### CI/CD Guidelines
- Use GitHub Actions for continuous integration
- Automated tests must pass before merging code
- CI pipelines should build and test containers
- Follow container best practices (minimal images, security scanning)

### Development Workflow
- Use feature branches for development
- Submit pull requests for code review
- Document API endpoints and data models
- Design with mobile and web clients in mind
- Document API endpoints thoroughly
- Keep dependencies updated and minimal