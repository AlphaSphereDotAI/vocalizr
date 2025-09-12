# 📦 Installation Guide

This guide provides detailed instructions for installing Vocalizr on various platforms and environments.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
  - [Docker (Recommended)](#docker-recommended)
  - [pip Install](#pip-install)
  - [From Source](#from-source)
  - [Development Setup](#development-setup)
- [Verification](#verification)
- [GPU Support](#gpu-support)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.12 or higher (for non-Docker installations)
- **Memory**: 4GB RAM
- **Storage**: 2GB free space for models and cache
- **Network**: Internet connection for initial model download

### Recommended Requirements
- **Memory**: 8GB+ RAM for optimal performance
- **GPU**: CUDA-compatible GPU for faster generation
- **CPU**: Multi-core processor for better performance

## Installation Methods

### Docker (Recommended)

Docker is the easiest and most reliable way to run Vocalizr.

#### Prerequisites
- Docker installed on your system ([Get Docker](https://docs.docker.com/get-docker/))

#### Quick Start
```bash
# Pull and run the latest image
docker run -p 7860:7860 ghcr.io/alphaspheredotai/vocalizr:latest
```

#### Custom Configuration
```bash
# Run with custom environment variables
docker run -p 7860:7860 \
  -e GRADIO_SERVER_PORT=8080 \
  -e DEBUG=false \
  ghcr.io/alphaspheredotai/vocalizr:latest
```

#### With Volume Mounts
```bash
# Mount local directories for logs and results
docker run -p 7860:7860 \
  -v ./logs:/home/nonroot/logs \
  -v ./results:/home/nonroot/results \
  ghcr.io/alphaspheredotai/vocalizr:latest
```

#### Docker Compose
Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  vocalizr:
    image: ghcr.io/alphaspheredotai/vocalizr:latest
    ports:
      - "7860:7860"
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - GRADIO_SERVER_PORT=7860
      - DEBUG=false
    volumes:
      - ./logs:/home/nonroot/logs
      - ./results:/home/nonroot/results
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

### pip Install

#### Prerequisites
- Python 3.12 or higher
- pip package manager

#### Installation
```bash
# Install from PyPI
pip install vocalizr

# Or install with specific version
pip install vocalizr==0.0.1
```

#### Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv vocalizr-env

# Activate virtual environment
# On Linux/macOS:
source vocalizr-env/bin/activate
# On Windows:
vocalizr-env\Scripts\activate

# Install vocalizr
pip install vocalizr
```

#### Running
```bash
# Start the application
vocalizr

# Or run as module
python -m vocalizr
```

### From Source

#### Prerequisites
- Python 3.12 or higher
- Git
- uv package manager (recommended) or pip

#### Clone Repository
```bash
git clone https://github.com/AlphaSphereDotAI/vocalizr.git
cd vocalizr
```

#### With uv (Recommended)
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies and install
uv sync
uv run vocalizr
```

#### With pip
```bash
# Install in development mode
pip install -e .

# Run the application
vocalizr
```

### Development Setup

For contributors and developers who want to modify the code:

#### Prerequisites
- All requirements from "From Source" installation
- Git

#### Setup
```bash
# Clone the repository
git clone https://github.com/AlphaSphereDotAI/vocalizr.git
cd vocalizr

# Install with development dependencies
pip install -e ".[dev]"

# Or with uv
uv sync --group dev
```

#### Development Tools
```bash
# Run linting
ruff check src/

# Format code
ruff format src/

# Type checking (if configured)
mypy src/
```

## Verification

After installation, verify that Vocalizr is working correctly:

### Command Line Test
```bash
# Test import
python -c "import vocalizr; print('Vocalizr imported successfully')"

# Check version
python -c "import vocalizr; print(vocalizr.__version__)"
```

### Web Interface Test
1. Start the application:
   ```bash
   vocalizr
   ```

2. Open your browser and navigate to:
   - Local: `http://localhost:7860`
   - Custom port: `http://localhost:[YOUR_PORT]`

3. You should see the Vocalizr web interface

### API Test
```python
from vocalizr.model import generate_audio_for_text

# Test audio generation
for sample_rate, audio_data in generate_audio_for_text(
    text="Hello, Vocalizr is working!",
    voice="af_heart"
):
    print(f"Generated audio: {len(audio_data)} samples at {sample_rate}Hz")
    break  # Just test the first chunk
```

## GPU Support

Vocalizr automatically detects and uses CUDA-compatible GPUs when available.

### NVIDIA GPU Setup
1. Install NVIDIA drivers
2. Install CUDA toolkit
3. Install PyTorch with CUDA support:
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/cu124
   ```

### Verification
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA devices: {torch.cuda.device_count()}")
```

## Troubleshooting

### Common Issues

#### 1. Python Version Error
```
ERROR: Python 3.12 or higher is required
```
**Solution**: Upgrade Python to version 3.12 or higher.

#### 2. Network Connection Error
```
Failed to resolve 'huggingface.co'
```
**Solution**: Check internet connection. Vocalizr needs to download models on first run.

#### 3. Permission Denied (Docker)
```
Permission denied while trying to connect to Docker daemon
```
**Solution**: Add your user to the docker group or run with `sudo`.

#### 4. Port Already in Use
```
OSError: [Errno 98] Address already in use
```
**Solution**: Change the port or stop the conflicting service:
```bash
# Change port
GRADIO_SERVER_PORT=8080 vocalizr

# Or kill process using port 7860
sudo lsof -t -i:7860 | xargs kill -9
```

#### 5. Out of Memory Error
```
CUDA out of memory
```
**Solution**: 
- Reduce batch size
- Use CPU instead of GPU
- Add more GPU memory

### Getting Help

If you encounter issues not covered here:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search [existing issues](https://github.com/AlphaSphereDotAI/vocalizr/issues)
3. Create a [new issue](https://github.com/AlphaSphereDotAI/vocalizr/issues/new) with:
   - Your operating system
   - Python version
   - Installation method used
   - Full error message
   - Steps to reproduce

## Next Steps

After successful installation:

- Read the [Usage Guide](USAGE.md) to learn how to use Vocalizr
- Explore the [API Documentation](API.md) for programmatic usage
- Check the [Configuration Guide](CONFIGURATION.md) for customization options
- Review [Examples](EXAMPLES.md) for common use cases