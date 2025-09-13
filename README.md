---
title: Vocalizr
emoji: 🔊
colorFrom: purple
colorTo: yellow
sdk: docker
app_port: 7860
---

# 🔊 Vocalizr

**A professional AI-powered voice generation application for high-quality text-to-speech synthesis**

[![Code Quality](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/code_quality.yaml/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/code_quality.yaml)
[![CodeQL](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/github-code-scanning/codeql)
[![Dependabot Updates](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/dependabot/dependabot-updates)
[![Docker Images](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/docker.yaml/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/docker.yaml)
[![GitHub Release](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/github.yaml/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/github.yaml)
[![Push to HuggingFace](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/huggingface.yaml/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/huggingface.yaml)
[![Upgrade Trunk Check](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/trunk_upgrade.yaml/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/trunk_upgrade.yaml)
[![Upload Python Package](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/pypi.yaml/badge.svg)](https://github.com/AlphaSphereDotAI/vocalizr/actions/workflows/pypi.yaml)

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

### Using pip

```bash
# Install the package
pip install vocalizr

# Launch the application
vocalizr
```

### Using Python

```python
from vocalizr.model import generate_audio_for_text

# Generate audio from text
for sample_rate, audio_data in generate_audio_for_text(
    text="Hello, this is Vocalizr!",
    voice="af_heart",
    speed=1.0
):
    # Process audio data
    print(f"Generated audio with sample rate: {sample_rate}")
```

## 🎯 Use Cases

- **Content Creation**: Generate voiceovers for videos, podcasts, and presentations
- **Accessibility**: Convert text content to audio for visually impaired users
- **Language Learning**: Create pronunciation examples and listening exercises
- **Chatbots & Virtual Assistants**: Add voice capabilities to conversational AI
- **Interactive Applications**: Enhance user experience with dynamic voice feedback
- **Audio Books**: Convert written content to spoken audio

## 🎭 Available Voices

| Voice ID | Description | Accent | Gender |
|----------|-------------|---------|--------|
| `af_heart` | Heart ❤️ | American | Female |
| `af_bella` | Bella 🔥 | American | Female |
| `af_nicole` | Nicole 🎧 | American | Female |
| `bf_emma` | Emma | British | Female |
| `am_michael` | Michael | American | Male |
| `bm_george` | George | British | Male |
| *...and 14 more voices* | | | |

*See [Voice Reference](docs/VOICES.md) for complete list and audio samples*

## 📚 Documentation

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

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details on how to get started.

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Kokoro AI Model**: Built on the powerful Kokoro text-to-speech engine
- **Gradio**: Enabling the intuitive web interface
- **AlphaSphere.AI**: Part of the comprehensive Character Backend ecosystem

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/AlphaSphereDotAI/vocalizr/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/AlphaSphereDotAI/vocalizr/discussions)
- 📧 **Contact**: [mohamed.hisham.abdelzaher@gmail.com](mailto:mohamed.hisham.abdelzaher@gmail.com)

---

<p align="center">
  <strong>🌟 If you find Vocalizr useful, please consider giving it a star! 🌟</strong>
</p>
