# Contributing to Media Processor

Thank you for your interest in contributing to Media Processor! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/media-processor.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install in development mode: `pip install -e .`

## Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black

# Run tests
python test_cli.py

# Format code
black src/ cli.py

# Lint code
flake8 src/ cli.py
```

## Adding New Features

### Adding a New Processing Tool

1. Create a new module in `src/category/your_tool.py`
2. Implement a class with a `process()` method
3. Add the command to `cli.py`
4. Update documentation in README.md
5. Add tests

Example structure:
```python
class YourProcessor:
    def __init__(self, **options):
        self.options = options
    
    def process(self, input_path, output_path=None):
        # Implementation here
        pass
```

### Adding Support for New Formats

1. Update the relevant processor class
2. Add format validation
3. Update documentation
4. Add test cases

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to all public methods
- Keep functions focused and small
- Use meaningful variable names

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Test on multiple platforms if possible

## Submitting Pull Requests

1. Ensure your code follows the style guidelines
2. Add tests for new functionality
3. Update documentation as needed
4. Commit with clear, descriptive messages
5. Push to your fork and submit a PR

### PR Title Format
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for code refactoring
- `test:` for test additions/changes

## Reporting Issues

- Use the issue tracker
- Provide clear reproduction steps
- Include system information
- Attach relevant logs or screenshots

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive criticism
- Help others learn and grow

Thank you for contributing!