# 🔊 Vocalizr

<p align="center">
  <strong>A professional AI-powered voice generation application for high-quality text-to-speech synthesis</strong>
</p>

<div align="center">

[![Build](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/build.yaml/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/build.yaml)
[![CI Tools](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/ci_tools.yaml/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/ci_tools.yaml)
[![CodeQL](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/github-code-scanning/codeql)
[![Dependabot Updates](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/dependabot/dependabot-updates)
[![Release](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/release.yaml/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/release.yaml)
[![Test](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/test.yaml/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/test.yaml)

</div>

Vocalizr is a state-of-the-art voice generation application that transforms text into natural-sounding speech using the powerful Kokoro AI model. Part of the Character Backend ecosystem, it provides both a user-friendly web interface and a robust API for seamless integration into larger applications.

## ✨ Features

- **🎭 Multiple Voice Personas**: Choose from 20+ distinct voice options including American and British accents, male and female voices
- **🚀 GPU Acceleration**: Automatic CUDA detection and utilization for high-performance generation
- **🌐 Web Interface**: Intuitive Gradio-based interface for easy interaction
- **🔧 Configurable Parameters**: Adjust speed, character limits, and file output options
- **📁 File Export**: Save generated audio as WAV files for offline use
- **🐳 Docker Support**: Ready-to-deploy containerized application
- **📊 Real-time Streaming**: Live audio generation and playback
- **🛡️ Production Ready**: Comprehensive monitoring, logging, and error handling

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Pull and run the latest image
docker run -p 7860:7860 ghcr.io/alphaspheredotai/vocalizr:latest

# Access the web interface at http://localhost:7860
```

### Using uv

```bash
uvx vocalizr
```

## 📚 Documentation

- **[Voice Reference](docs/VOICES.md)** - for complete list of voice ids
- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions for all platforms
- **[Usage Guide](docs/USAGE.md)** - Web interface and CLI usage examples
- **[API Reference](docs/API.md)** - Complete API documentation for developers
- **[Configuration](docs/CONFIGURATION.md)** - Environment variables and settings
- **[Development Guide](docs/DEVELOPMENT.md)** - Contributing and architecture overview
- **[Examples](docs/EXAMPLES.md)** - Code examples and tutorials
- **[Deployment](docs/DEPLOYMENT.md)** - Production deployment guide
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🛠️ System Requirements

- **Python**: 3.12 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space for models and cache
- **GPU**: CUDA-compatible GPU (optional, for faster generation)
- **Network**: Internet connection for initial model download

## 📄 License

This project is licensed under the MIT License. See [LICENSE](docs/LICENSE.md) for details.

## 🙏 Acknowledgments

- **Kokoro AI Model**: Built on the powerful Kokoro text-to-speech engine
- **Gradio**: Enabling the intuitive web interface
- **AlphaSphere.AI**: Part of the comprehensive Character Backend ecosystem

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/AlphaSphereDotAI/vocalizr/issues)
- 📧 **Contact**: [alphasphere.ai@gmail.com](mailto:alphasphere.ai@gmail.com)

---

<p align="center">
  <strong>🌟 If you find Vocalizr useful, please consider giving it a star! 🌟</strong>
</p>
