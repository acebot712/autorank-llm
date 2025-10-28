# Contributing to AutoRank-LLM

Thank you for your interest in contributing to AutoRank-LLM! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, professional, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Verify the bug on the latest version

Include in your bug report:
- Python version
- Operating system
- Minimal code to reproduce the issue
- Expected vs actual behavior
- Full error traceback

### Suggesting Features

Feature requests are welcome! Please:
1. Check existing feature requests first
2. Clearly describe the use case
3. Explain why this feature would be useful
4. Consider implementation complexity

### Pull Requests

#### Setup Development Environment

```bash
git clone https://github.com/acebot712/autorank-llm.git
cd autorank-llm
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

#### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write tests**
   - Add tests for new functionality
   - Ensure all tests pass: `python -m unittest discover tests`

3. **Follow code style**
   - Follow PEP 8
   - Use type hints where appropriate
   - Add docstrings to public functions/classes

4. **Update documentation**
   - Update README.md if adding user-facing features
   - Add docstrings to new code
   - Update CHANGELOG.md

5. **Commit with clear messages**
   ```
   Add feature: brief description

   - Detailed point 1
   - Detailed point 2
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

#### PR Checklist

- [ ] Tests pass locally
- [ ] Code follows PEP 8
- [ ] Added tests for new code
- [ ] Updated documentation
- [ ] Updated CHANGELOG.md
- [ ] Commit messages are clear

## Development Guidelines

### Code Style

- Follow PEP 8
- Max line length: 127 characters
- Use meaningful variable names
- Add type hints to function signatures

### Testing

- Write unit tests for all new functionality
- Aim for high test coverage
- Use descriptive test names
- Mock external dependencies

### Documentation

- Add docstrings to all public functions/classes
- Use Google-style docstrings
- Update README for user-facing changes
- Add examples for new features

## Questions?

Open an issue with the `question` label or start a discussion.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
