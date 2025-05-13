---
name: ShowstockTesting
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - "run tests"
  - "testing"
  - "test coverage"
  - "pytest"
  - "run the tests"
---

# Showstock Testing Guide

This microagent provides information about running tests for the Showstock project.

## Testing Overview

Showstock uses pytest for testing with the following features:
- Automated test discovery in the `tests` directory
- Test coverage reporting with pytest-cov
- Asynchronous test support with pytest-asyncio
- PostgreSQL database integration for testing

## Running Tests

Tests should only be run using Docker:

```bash
# Run tests with coverage
docker compose -f docker/compose.yaml up tests
```

This will:
1. Build a test container using `docker/Dockerfile.tests`
2. Start a PostgreSQL database container
3. Run all tests with coverage reporting
4. Generate coverage reports in XML and terminal output

## Test Configuration

The test configuration is defined in `pytest.ini`:
- Tests are automatically discovered in the `tests` directory
- Test files must match the pattern `test_*.py`
- Test functions must start with `test_`
- Asyncio mode is set to `auto` for async test support
- Coverage reports are generated for the `showstock` package

## Database Configuration for Tests

Tests require a PostgreSQL database. The connection can be configured using environment variables:
- `SHOWSTOCK_DB_HOST`: Database host (default: localhost)
- `SHOWSTOCK_DB_PORT`: Database port (default: 5432)
- `SHOWSTOCK_DB_USER`: Database user (default: postgres)
- `SHOWSTOCK_DB_PASSWORD`: Database password (default: postgres)
- `SHOWSTOCK_DB_NAME`: Database name (default: showstock_test)

Alternatively, you can set the full database URL:
- `DATABASE_URL`: Full PostgreSQL connection string

## CI/CD Integration

Tests are automatically run on GitHub Actions:
- On every push to the main branch
- On every pull request to the main branch
- Coverage reports are uploaded to Codecov.io

## Troubleshooting

If tests fail due to database connection issues:
1. Ensure Docker and Docker Compose are properly installed
2. Verify the PostgreSQL service is running in Docker
3. Check the database connection settings in the Docker Compose file
4. Ensure the database container is healthy and accessible