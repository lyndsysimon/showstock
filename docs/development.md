# Development Guide

## Prerequisites

- Python 3.12+
- PostgreSQL
- Git

## Setup

1. Clone the repository:
```bash
git clone https://github.com/lyndsysimon/showstock.git
cd showstock
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
alembic upgrade head
```

## Running Tests

```bash
pytest
```

## Code Style

We use:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run all checks:
```bash
pre-commit run --all-files
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests and checks
4. Submit a pull request 