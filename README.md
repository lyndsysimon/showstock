# Showstock

[![Test](https://github.com/lyndsysimon/showstock/actions/workflows/test.yml/badge.svg)](https://github.com/lyndsysimon/showstock/actions/workflows/test.yml)
[![Lint](https://github.com/lyndsysimon/showstock/actions/workflows/lint.yml/badge.svg)](https://github.com/lyndsysimon/showstock/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/lyndsysimon/showstock/branch/main/graph/badge.svg)](https://codecov.io/gh/lyndsysimon/showstock)

Nutrition management for show livestock

## Features

- FastAPI web application
- SQLAlchemy ORM with async support
- PostgreSQL database with connection pooling
- Environment-based configuration

## Development

### Prerequisites

- Docker
- Docker Compose

### Configuration

The application is configured using environment variables. Copy the `.env.example` file to `.env` and adjust the values as needed:

```bash
cp .env.example .env
# Edit .env with your preferred editor
```

### Running the Application

```bash
# Start the application and database
docker compose -f docker/compose.yaml up app db
```

The application will be available at http://localhost:8000 by default.

### Running Tests

```bash
# Run tests with coverage
docker compose -f docker/compose.yaml up tests
```

## Development Setup

To set up your development environment:

```bash
# Run the setup script to install dev dependencies and pre-commit hooks
./setup_dev.sh
```

This will install all development dependencies and set up pre-commit hooks to ensure code quality.

### Code Formatting

This project uses Black for code formatting. Code will be automatically formatted when you commit changes thanks to pre-commit hooks.

You can also run Black manually:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .
```

## CI/CD

This project uses GitHub Actions for continuous integration:

- Tests are run automatically on every push and pull request
- Code coverage reports are generated and uploaded to Codecov.io
- Code formatting is checked using Black
