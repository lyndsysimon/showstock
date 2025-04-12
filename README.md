# Showstock

[![Test](https://github.com/lyndsysimon/showstock/actions/workflows/test.yml/badge.svg)](https://github.com/lyndsysimon/showstock/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/lyndsysimon/showstock/branch/main/graph/badge.svg)](https://codecov.io/gh/lyndsysimon/showstock)

Nutrition management for show livestock

## Development

### Prerequisites

- Docker
- Docker Compose

### Running the Application

```bash
# Start the application and database
docker compose -f docker/compose.yaml up app db
```

### Running Tests

```bash
# Run tests with coverage
docker compose -f docker/compose.yaml up tests
```

## CI/CD

This project uses GitHub Actions for continuous integration:

- Tests are run automatically on every push and pull request
- Code coverage reports are generated and uploaded to Codecov.io
