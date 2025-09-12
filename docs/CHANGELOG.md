# 📝 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive professional documentation suite
- Installation guide with multiple deployment methods
- Usage guide for web interface, CLI, and Python API
- Complete API documentation with integration examples
- Configuration guide for environment variables and deployment
- Development guide with architecture and contribution workflow
- Examples and tutorials for common use cases
- Deployment guide for production environments
- Troubleshooting guide for common issues
- Contributing guidelines and code of conduct

### Changed
- Enhanced README.md with professional overview and features
- Improved project structure with organized documentation

### Documentation
- Added comprehensive documentation covering all aspects of the project
- Included practical examples for various use cases
- Provided detailed troubleshooting and support information

## [0.0.1] - 2024-01-15

### Added
- Initial release of Vocalizr voice generation application
- Gradio web interface for text-to-speech conversion
- Support for 20+ voice personas (American and British accents)
- Command-line interface for easy deployment
- Python API for programmatic usage
- Docker support for containerized deployment
- CUDA GPU acceleration support
- Configurable speed and character limit settings
- Audio file export functionality (WAV format)
- Real-time streaming audio generation
- Comprehensive logging and error handling

### Features
- **Voice Selection**: Multiple voice options with different personalities
  - American female voices: Heart, Bella, Nicole, Aoede, Kore, Sarah, Nova, Sky, Alloy, Jessica, River
  - American male voices: Michael, Fenrir, Puck, Echo, Eric, Liam, Onyx, Santa, Adam
  - British female voices: Emma, Isabella, Alice, Lily
  - British male voices: George, Fable, Lewis, Daniel

- **Web Interface**: Intuitive Gradio-based interface with:
  - Text input with character limit control
  - Voice selection dropdown
  - Speed adjustment slider (0.5x to 2.0x)
  - Hardware detection and display
  - Real-time audio generation and playback
  - Audio file download capability

- **API Features**:
  - Generator-based audio streaming
  - Configurable voice and speed parameters
  - Optional file saving
  - Debug mode support
  - Error handling and validation

- **Technical Specifications**:
  - Built on Kokoro AI text-to-speech model
  - 24kHz audio output sample rate
  - Float32 audio data format
  - Automatic CUDA detection and usage
  - Environment-based configuration
  - Structured logging with Loguru

### Technical Details
- **Framework**: Gradio for web interface
- **AI Model**: Kokoro 82M parameter model
- **Audio Processing**: soundfile for WAV file operations
- **Backend**: PyTorch with CUDA support
- **Configuration**: Environment variable based
- **Containerization**: Docker with multi-stage build
- **Package Management**: uv for dependency management

### Infrastructure
- GitHub Actions CI/CD workflows
- Docker image publishing to GitHub Container Registry
- Automated code quality checks with Ruff
- Dependabot for dependency updates
- CodeQL security scanning
- Automated testing and linting

### Dependencies
- `gradio[mcp]>=5.38.0` - Web interface framework
- `kokoro>=0.9.4` - Text-to-speech AI model
- `soundfile>=0.13.1` - Audio file processing
- `pip>=25.1.1` - Package installer

### Development Dependencies
- `ruff>=0.11.12` - Code formatting and linting
- `ty>=0.0.1a10` - Type checking utilities

### Known Issues
- Requires internet connection for initial model download
- GPU acceleration requires CUDA-compatible hardware
- Large memory usage for longer text inputs

### Breaking Changes
- None (initial release)

---

## Release Notes Format

For future releases, we follow this format:

### Version Types
- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backwards compatible
- **Patch** (0.0.X): Bug fixes, backwards compatible

### Change Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes

### Unreleased Section
- Keep track of changes not yet released
- Move to versioned section on release
- Follow semantic versioning principles

---

## Contributing to Changelog

When contributing to the project:

1. **Add entries** to the `[Unreleased]` section
2. **Use appropriate categories** (Added, Changed, Fixed, etc.)
3. **Write clear descriptions** of changes
4. **Reference issues/PRs** where relevant
5. **Follow the format** established in previous entries

### Example Entry Format

```markdown
### Added
- New batch processing API endpoint for multiple text inputs (#123)
- Support for custom voice models via configuration (#124)

### Fixed
- Memory leak in audio generation pipeline (#125)
- Incorrect sample rate handling for certain voices (#126)

### Changed
- Improved error messages for invalid input validation (#127)
- Updated Gradio to version 5.45.0 for better performance (#128)
```

---

## Upgrade Guide

### From Future Versions

Instructions for upgrading between versions will be provided here as they become available.

### Breaking Changes Policy

We are committed to minimizing breaking changes. When they are necessary:

1. **Advance notice** will be given (at least one minor version)
2. **Migration guides** will be provided
3. **Deprecation warnings** will be added first
4. **Alternative approaches** will be documented

---

## Support and Resources

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/AlphaSphereDotAI/vocalizr/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AlphaSphereDotAI/vocalizr/discussions)
- **Contact**: [mohamed.hisham.abdelzaher@gmail.com](mailto:mohamed.hisham.abdelzaher@gmail.com)

---

**Note**: This changelog is maintained by the project maintainers and community contributors. If you notice any missing or incorrect information, please [open an issue](https://github.com/AlphaSphereDotAI/vocalizr/issues) or [submit a pull request](https://github.com/AlphaSphereDotAI/vocalizr/pulls).