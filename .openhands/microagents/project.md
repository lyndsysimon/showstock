---
name: ShowStock Project Rules
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - showstock
  - livestock nutrition
  - show livestock
  - project rules
  - development guidelines
  - containerization
  - async python
---

# ShowStock Project Rules Microagent

This microagent provides guidelines and rules for the ShowStock project, a web backend for a mobile and web application designed to help livestock owners develop and implement nutrition plans for their show livestock.

## Project Overview

ShowStock is a web backend application that will:
- Support mobile and web frontends
- Help livestock owners manage nutrition for show animals
- Provide tools for developing and implementing feeding plans
- Track nutritional data and animal performance

## Technical Rules and Guidelines

### Asynchronous Python Development
- **Rule 1**: All code must be written using asynchronous Python patterns
- **Rule 2**: Dependencies must support fully asynchronous use
- **Rule 3**: Only async code should be called when serving web requests
- **Rule 4**: Use `async`/`await` syntax consistently throughout the codebase
- **Rule 5**: Avoid blocking operations in request handlers

### Containerization Requirements
- **Rule 6**: The project must be entirely containerized
- **Rule 7**: Never create Python environments directly on the host
- **Rule 8**: All commands must be run inside the appropriate container
- **Rule 9**: Use Docker for containerization
- **Rule 10**: Use Docker Compose for container orchestration
- **Rule 11**: Container configurations should be version controlled

### CI/CD Guidelines
- **Rule 12**: Use GitHub Actions for continuous integration
- **Rule 13**: Automated tests must pass before merging code
- **Rule 14**: CI pipelines should build and test containers
- **Rule 15**: Follow container best practices (minimal images, security scanning)

### Development Workflow
- **Rule 16**: Use feature branches for development
- **Rule 17**: Submit pull requests for code review
- **Rule 18**: Document API endpoints and data models
- **Rule 19**: Write tests for all new functionality
- **Rule 20**: Follow async Python best practices

## Best Practices

- Design with mobile and web clients in mind
- Document API endpoints thoroughly
- Implement proper error handling for async code
- Use type hints throughout the codebase
- Follow container security best practices
- Keep dependencies updated and minimal
- Write comprehensive tests for async code
