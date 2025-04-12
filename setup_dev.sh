#!/bin/bash
set -e

# Check if uv is installed, if not install it
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

echo "Development environment setup complete!"
echo "Pre-commit hooks have been installed. They will run automatically on git commit."
echo "You can also run them manually with: pre-commit run --all-files"
