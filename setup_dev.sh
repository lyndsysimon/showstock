#!/bin/bash
set -e

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

echo "Development environment setup complete!"
echo "Pre-commit hooks have been installed. They will run automatically on git commit."
echo "You can also run them manually with: pre-commit run --all-files"
