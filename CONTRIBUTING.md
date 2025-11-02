# Contributing to imgbb-sdk

Thank you for your interest in contributing to imgbb-sdk! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip or poetry

### Setting Up Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/imgbb-sdk.git
   cd imgbb-sdk
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Set up pre-commit hooks (optional but recommended)**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## 🔧 Development Workflow

### Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes**
   - Write your code
   - Add or update tests
   - Update documentation if needed

3. **Run tests**
   ```bash
   pytest
   ```

4. **Check code quality**
   ```bash
   # Format code
   black src tests
   
   # Lint code
   ruff check src tests
   
   # Type check
   mypy src
   ```

### Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `style:` - Code style changes (formatting, etc.)
- `chore:` - Maintenance tasks

Example:
```bash
git commit -m "feat: add support for custom timeout configuration"
git commit -m "fix: handle empty file objects correctly"
git commit -m "docs: update API reference with new examples"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=imgbb_sdk --cov-report=html

# Run only unit tests (skip integration tests)
pytest -m "not integration"

# Run specific test file
pytest tests/test_client.py

# Run specific test
pytest tests/test_client.py::TestValidation::test_empty_api_key
```

### Integration Tests

Integration tests require a valid ImgBB API key:

```bash
export IMGBB_API_KEY="your-api-key"
pytest -m integration
```

> **Note**: Integration tests make real API calls and may count against your rate limit.

### Code Quality Tools

#### Black (Code Formatting)
```bash
# Check formatting
black --check src tests

# Format code
black src tests
```

#### Ruff (Linting)
```bash
# Check for issues
ruff check src tests

# Auto-fix issues
ruff check --fix src tests
```

#### Mypy (Type Checking)
```bash
# Run type checker
mypy src

# Run with verbose output
mypy src --show-error-codes
```

## 📝 Pull Request Process

1. **Update documentation**
   - Update README.md if you've added new features
   - Add docstrings to new functions/classes
   - Update CHANGELOG.md with your changes

2. **Ensure all checks pass**
   - All tests must pass
   - Code coverage should not decrease
   - Linting and formatting checks must pass

3. **Create a Pull Request**
   - Use a clear, descriptive title
   - Reference any related issues
   - Describe what you've changed and why
   - Include screenshots/examples if applicable

4. **Code Review**
   - Address any feedback from reviewers
   - Keep the PR focused on a single feature/fix
   - Be responsive to comments

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] CHANGELOG.md updated
```

## 🐛 Bug Reports

### Before Submitting

- Check existing issues to avoid duplicates
- Test with the latest version
- Provide a minimal reproducible example

### Bug Report Template

```markdown
**Describe the bug**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. ...
2. ...
3. ...

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- imgbb-sdk version: [e.g., 1.0.0]

**Additional context**
Any other relevant information.
```

## ✨ Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Any other context about the feature request.
```

## 📖 Documentation

- Use clear, concise language
- Include code examples where applicable
- Update docstrings using Google-style format:

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param2 is negative
    
    Example:
        >>> example_function("test", 42)
        True
    """
    pass
```

## 🎯 Code Style

### Python Style Guide

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints for all functions
- Maximum line length: 100 characters
- Use descriptive variable names
- Add comments for complex logic

### Example

```python
from typing import Optional, Union
from pathlib import Path


def process_image(
    image_path: Union[str, Path],
    max_size: int = 1024,
    quality: Optional[int] = None
) -> bytes:
    """Process an image file.
    
    Args:
        image_path: Path to the image file
        max_size: Maximum dimension (width or height) in pixels
        quality: JPEG quality (1-100), None for default
    
    Returns:
        Processed image as bytes
    
    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If quality is out of range
    """
    if quality is not None and not 1 <= quality <= 100:
        raise ValueError("Quality must be between 1 and 100")
    
    # Implementation...
    pass
```

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible new features
- **PATCH** version for backwards-compatible bug fixes

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤔 Questions?

- Open an issue for questions
- Join discussions in GitHub Discussions
- Contact: mail@supratim.me

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- CHANGELOG.md

Thank you for contributing to imgbb-sdk! 🎉
