# 🤝 Contributing to Vocalizr

Thank you for your interest in contributing to Vocalizr! This guide will help you get started with contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)
- [Community Guidelines](#community-guidelines)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

### Summary

- **Be respectful** and inclusive
- **Be collaborative** and constructive
- **Be mindful** of your words and actions
- **Be helpful** to newcomers and experienced contributors alike

## Getting Started

### Ways to Contribute

We welcome various types of contributions:

- 🐛 **Bug reports** - Help us identify and fix issues
- 💡 **Feature requests** - Suggest new functionality
- 📖 **Documentation** - Improve or add documentation
- 🧪 **Testing** - Add or improve tests
- 🔧 **Code contributions** - Fix bugs or implement features
- 🎨 **Design** - Improve UI/UX of the web interface
- 🌍 **Localization** - Add support for new languages/voices
- 📝 **Examples** - Create tutorials and examples

### Prerequisites

Before contributing, ensure you have:

- **Git** installed and configured
- **Python 3.12+** installed
- **Basic knowledge** of Python and web development
- **Familiarity** with the project structure (see [Development Guide](docs/DEVELOPMENT.md))

## How to Contribute

### 1. Find an Issue

Start by looking at our [issues page](https://github.com/AlphaSphereDotAI/vocalizr/issues):

- 🏷️ **Good first issue** - Perfect for newcomers
- 🆘 **Help wanted** - Issues where we need assistance
- 🐛 **Bug** - Confirmed bugs that need fixing
- ✨ **Enhancement** - New features or improvements

### 2. Fork the Repository

1. Click the "Fork" button on the [repository page](https://github.com/AlphaSphereDotAI/vocalizr)
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/vocalizr.git
   cd vocalizr
   ```

### 3. Create a Branch

Create a descriptive branch name:

```bash
# For bug fixes
git checkout -b fix/memory-leak-in-audio-generation

# For new features
git checkout -b feature/add-batch-processing

# For documentation
git checkout -b docs/improve-api-documentation
```

### Branch Naming Conventions

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation changes
- `test/description` - Test additions/improvements
- `refactor/description` - Code refactoring
- `chore/description` - Maintenance tasks

## Development Setup

### 1. Set Up Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -e ".[dev]"

# Or with uv
uv sync --group dev
```

### 2. Install Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Set up git hooks
pre-commit install
```

### 3. Verify Setup

```bash
# Run tests
pytest

# Check code quality
ruff check src/
ruff format src/

# Start the application
python -m vocalizr
```

## Coding Standards

### Code Style

We use **Ruff** for code formatting and linting:

```bash
# Format code
ruff format src/

# Check for issues
ruff check src/

# Fix auto-fixable issues
ruff check --fix src/
```

### Type Hints

All functions should include comprehensive type hints:

```python
from typing import Generator, Literal, Any
from numpy import ndarray, dtype, float32

def generate_audio_for_text(
    text: str,
    voice: str = "af_heart",
    speed: float = 1.0,
    save_file: bool = False,
    debug: bool = False,
    char_limit: int = -1,
) -> Generator[
    tuple[Literal[24000], ndarray[tuple[float32], dtype[float32]]],
    Any,
    None,
]:
    """Generate audio from text with proper type annotations."""
    # Implementation here
```

### Documentation

#### Docstring Format

Use Google-style docstrings:

```python
def complex_function(
    param1: str,
    param2: int,
    param3: bool = False
) -> tuple[str, int]:
    """
    Brief description of what the function does.
    
    Longer description with more details about the function's purpose,
    algorithms used, or any important considerations.
    
    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter.
        param3: Description of the optional parameter. Defaults to False.
    
    Returns:
        A tuple containing:
            - str: Description of first return value
            - int: Description of second return value
    
    Raises:
        ValueError: If param1 is empty.
        RuntimeError: If param2 is negative.
    
    Example:
        >>> result = complex_function("hello", 42)
        >>> print(result)
        ('hello_processed', 42)
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    
    if param2 < 0:
        raise RuntimeError("param2 must be non-negative")
    
    return f"{param1}_processed", param2
```

#### Code Comments

- Use comments to explain **why**, not what
- Keep comments concise and up-to-date
- Use TODO comments for future improvements

```python
# Good: Explains why
# Use exponential backoff to handle temporary API failures
retry_delay *= 2

# Bad: Explains what (obvious from code)
# Multiply retry_delay by 2
retry_delay *= 2
```

### Testing

#### Test Structure

```python
import pytest
from unittest.mock import patch, MagicMock
from vocalizr.model import generate_audio_for_text

class TestGenerateAudioForText:
    """Test suite for the generate_audio_for_text function."""
    
    def test_basic_generation(self):
        """Test basic audio generation functionality."""
        # Arrange
        text = "Hello, world!"
        expected_voice = "af_heart"
        
        # Act
        with patch('vocalizr.model.PIPELINE') as mock_pipeline:
            mock_pipeline.return_value = [(None, None, np.array([0.1, 0.2]))]
            results = list(generate_audio_for_text(text, voice=expected_voice))
        
        # Assert
        assert len(results) > 0
        sample_rate, audio = results[0]
        assert sample_rate == 24000
        assert isinstance(audio, np.ndarray)
    
    @pytest.mark.parametrize("invalid_text", ["", "   ", "abc"])
    def test_invalid_text_input(self, invalid_text):
        """Test handling of invalid text inputs."""
        with pytest.raises(Exception):
            list(generate_audio_for_text(invalid_text))
    
    def test_voice_parameter_validation(self):
        """Test that voice parameter is properly validated."""
        # Test with valid voice
        with patch('vocalizr.model.PIPELINE'):
            list(generate_audio_for_text("test", voice="af_heart"))
        
        # Test with invalid voice should still work (handled gracefully)
        with patch('vocalizr.model.PIPELINE'):
            list(generate_audio_for_text("test", voice="invalid_voice"))
```

#### Test Guidelines

- **Arrange-Act-Assert** pattern
- **Descriptive test names** that explain what is being tested
- **Parameterized tests** for multiple input scenarios
- **Mock external dependencies** (network calls, file system)
- **Test edge cases** and error conditions

### Performance Considerations

- **Memory efficiency**: Clean up resources after use
- **CPU optimization**: Use efficient algorithms
- **GPU utilization**: Leverage CUDA when available
- **Caching**: Implement appropriate caching strategies

```python
import gc
import torch

def memory_efficient_function():
    """Example of memory-efficient implementation."""
    try:
        # Main logic here
        result = process_data()
        return result
    finally:
        # Clean up resources
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
```

## Submitting Changes

### 1. Commit Guidelines

#### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): brief description

Longer description explaining the change in more detail.
Include motivation for the change and contrast with previous behavior.

Fixes #123
```

#### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

#### Examples

```bash
# Good commit messages
git commit -m "feat(api): add batch processing endpoint"
git commit -m "fix(model): resolve memory leak in audio generation"
git commit -m "docs(readme): update installation instructions"

# Bad commit messages
git commit -m "fix stuff"
git commit -m "update code"
git commit -m "changes"
```

### 2. Pull Request Process

#### Before Submitting

- [ ] All tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] Branch is up-to-date with main

#### Pull Request Template

When creating a PR, use this template:

```markdown
## Description

Brief description of the changes made.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues

Fixes #(issue number)
Related to #(issue number)

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

## Screenshots (if applicable)

Add screenshots to help explain your changes.

## Checklist

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Additional Notes

Any additional information or context about the changes.
```

### 3. Draft Pull Requests

Use draft PRs for:

- **Work in progress** - Getting early feedback
- **Large changes** - Breaking down into smaller reviews
- **Experimental features** - Testing ideas

## Review Process

### What Reviewers Look For

#### Code Quality
- **Correctness**: Does the code work as intended?
- **Readability**: Is the code easy to understand?
- **Maintainability**: Can the code be easily modified?
- **Performance**: Are there any performance issues?

#### Design
- **Architecture**: Does the change fit the overall design?
- **API design**: Are new APIs well-designed and consistent?
- **Error handling**: Are errors handled appropriately?
- **Edge cases**: Are edge cases considered?

#### Testing
- **Coverage**: Are all code paths tested?
- **Quality**: Are tests well-written and reliable?
- **Integration**: Do tests work with the existing test suite?

### Responding to Feedback

#### How to Address Review Comments

1. **Read carefully** - Understand the feedback
2. **Ask questions** - If something is unclear
3. **Make changes** - Address the feedback
4. **Respond** - Let reviewers know what you've changed
5. **Be patient** - Reviews take time

#### Example Response

```markdown
Thanks for the review! I've addressed your comments:

1. **Memory leak in audio generation**: Fixed by adding proper cleanup in the finally block (commit abc123)
2. **Missing error handling**: Added try-catch for network errors (commit def456)
3. **Documentation**: Updated the docstring with examples (commit ghi789)

The failing test was due to a missing mock - fixed in commit jkl012.

Ready for another review!
```

### Review Timeline

- **Initial response**: Within 48 hours
- **Complete review**: Within 1 week
- **Follow-up reviews**: Within 24-48 hours

## Community Guidelines

### Communication

#### Be Respectful
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community

#### Be Helpful
- Help newcomers get started
- Share knowledge and resources
- Provide constructive feedback
- Be patient with questions

### Issue Etiquette

#### Reporting Bugs
- **Search first** - Check if the issue already exists
- **Use templates** - Fill out the bug report template
- **Provide details** - Include reproduction steps
- **Follow up** - Respond to questions from maintainers

#### Feature Requests
- **Explain the use case** - Why is this needed?
- **Consider alternatives** - Are there existing solutions?
- **Be open to feedback** - The feature might need adjustments

### Discussion Guidelines

#### GitHub Discussions
- **Use appropriate categories** - Help organize discussions
- **Search before posting** - Avoid duplicate discussions
- **Stay on topic** - Keep discussions focused
- **Be constructive** - Provide helpful input

#### Code Reviews
- **Be constructive** - Focus on improvement, not criticism
- **Explain reasoning** - Why should something change?
- **Suggest solutions** - Don't just point out problems
- **Acknowledge good work** - Recognize quality contributions

### Recognition

We recognize contributors in several ways:

- **Contributors list** in README
- **Release notes** mentioning contributors
- **Special recognition** for significant contributions
- **Maintainer status** for ongoing contributors

### Getting Help

If you need help with contributing:

1. **Check documentation** - Start with this guide and [Development Guide](docs/DEVELOPMENT.md)
2. **Search issues** - Someone might have had the same question
3. **Ask in discussions** - Use GitHub Discussions for questions
4. **Contact maintainers** - Reach out directly if needed

### Maintainer Responsibilities

Maintainers will:

- **Respond promptly** to issues and PRs
- **Provide clear feedback** on contributions
- **Maintain quality standards** while being welcoming
- **Guide contributors** through the process
- **Make decisions** fairly and transparently

### License

By contributing to Vocalizr, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Thank You! 🙏

We appreciate all contributions to Vocalizr, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

Every contribution makes the project better for everyone. Thank you for being part of the Vocalizr community!

---

**Questions?** Feel free to [open a discussion](https://github.com/AlphaSphereDotAI/vocalizr/discussions) or reach out to the maintainers.

**New to open source?** Check out [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/) for more guidance.