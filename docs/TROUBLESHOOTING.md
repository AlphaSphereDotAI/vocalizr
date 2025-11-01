# 🔧 Troubleshooting Guide

Comprehensive guide for diagnosing and resolving common issues with Vocalizr.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Installation Issues](#installation-issues)
- [Runtime Issues](#runtime-issues)
- [Performance Problems](#performance-problems)
- [Network & Connectivity](#network--connectivity)
- [Audio Generation Issues](#audio-generation-issues)
- [Docker & Container Issues](#docker--container-issues)
- [Deployment Issues](#deployment-issues)
- [Development Issues](#development-issues)
- [Getting Help](#getting-help)

## Quick Diagnostics

### System Information Checker

```python
#!/usr/bin/env python3
"""
Vocalizr System Diagnostics Script
Run this script to check your system compatibility and diagnose issues.
"""

import sys
import platform
import subprocess
import pkg_resources
import torch
import psutil
from pathlib import Path

def check_python_version():
    """Check Python version compatibility."""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 12):
        print("❌ Python 3.12+ required")
        return False
    else:
        print("✅ Python version compatible")
        return True

def check_system_resources():
    """Check system memory and CPU."""
    memory = psutil.virtual_memory()
    cpu_count = psutil.cpu_count()
    
    print(f"System Memory: {memory.total // (1024**3)} GB total, {memory.available // (1024**3)} GB available")
    print(f"CPU Cores: {cpu_count}")
    
    issues = []
    if memory.total < 4 * (1024**3):  # Less than 4GB
        issues.append("❌ Insufficient memory (4GB+ recommended)")
    else:
        print("✅ Sufficient memory available")
    
    if cpu_count < 2:
        issues.append("❌ Insufficient CPU cores (2+ recommended)")
    else:
        print("✅ Sufficient CPU cores")
    
    return len(issues) == 0, issues

def check_gpu_availability():
    """Check CUDA GPU availability."""
    try:
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory // (1024**3)
            
            print(f"✅ CUDA GPU Available: {gpu_name}")
            print(f"   GPU Memory: {gpu_memory} GB")
            print(f"   GPU Count: {gpu_count}")
            return True
        else:
            print("ℹ️  No CUDA GPU detected (CPU mode will be used)")
            return True
    except Exception as e:
        print(f"⚠️  GPU check failed: {e}")
        return False

def check_dependencies():
    """Check required dependencies."""
    required_packages = [
        'gradio',
        'kokoro',
        'soundfile',
        'torch',
        'numpy',
        'loguru'
    ]
    
    missing = []
    for package in required_packages:
        try:
            pkg_resources.get_distribution(package)
            print(f"✅ {package} installed")
        except pkg_resources.DistributionNotFound:
            missing.append(package)
            print(f"❌ {package} missing")
    
    return len(missing) == 0, missing

def check_network_connectivity():
    """Check network connectivity to required services."""
    test_urls = [
        'huggingface.co',
        'github.com'
    ]
    
    for url in test_urls:
        try:
            result = subprocess.run(
                ['ping', '-c', '1', url],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"✅ {url} reachable")
            else:
                print(f"❌ {url} unreachable")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"❌ Cannot test connectivity to {url}")

def check_file_permissions():
    """Check file system permissions."""
    test_dirs = [
        Path.cwd() / 'results',
        Path.cwd() / 'logs',
        Path.home() / '.cache'
    ]
    
    for test_dir in test_dirs:
        try:
            test_dir.mkdir(exist_ok=True)
            test_file = test_dir / 'test_write.tmp'
            test_file.write_text('test')
            test_file.unlink()
            print(f"✅ Write permissions OK: {test_dir}")
        except Exception as e:
            print(f"❌ Write permission denied: {test_dir} - {e}")

def main():
    """Run all diagnostic checks."""
    print("🔍 Vocalizr System Diagnostics")
    print("=" * 50)
    
    all_good = True
    
    print("\n📊 System Information:")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    
    print("\n🐍 Python Environment:")
    if not check_python_version():
        all_good = False
    
    print("\n💾 System Resources:")
    resources_ok, resource_issues = check_system_resources()
    if not resources_ok:
        all_good = False
        for issue in resource_issues:
            print(issue)
    
    print("\n🚀 GPU Support:")
    if not check_gpu_availability():
        all_good = False
    
    print("\n📦 Dependencies:")
    deps_ok, missing_deps = check_dependencies()
    if not deps_ok:
        all_good = False
        print("Missing packages:", ', '.join(missing_deps))
    
    print("\n🌐 Network Connectivity:")
    check_network_connectivity()
    
    print("\n📁 File Permissions:")
    check_file_permissions()
    
    print("\n" + "=" * 50)
    if all_good:
        print("✅ All checks passed! Your system should work with Vocalizr.")
    else:
        print("❌ Some issues detected. Please address the items marked with ❌.")
    
    print("\nFor help, visit: https://github.com/AlphaSphereDotAI/vocalizr/issues")

if __name__ == "__main__":
    main()
```

### Quick Health Check

```bash
#!/bin/bash
# Quick Vocalizr health check script

echo "🔍 Vocalizr Quick Health Check"
echo "================================"

# Check if Vocalizr is installed
echo "📦 Checking Vocalizr installation..."
if python -c "import vocalizr" 2>/dev/null; then
    echo "✅ Vocalizr is installed"
else
    echo "❌ Vocalizr is not installed or not importable"
    exit 1
fi

# Check if service is running
echo "🌐 Checking if Vocalizr service is running..."
if curl -s http://localhost:7860/health >/dev/null 2>&1; then
    echo "✅ Vocalizr service is responding"
else
    echo "ℹ️  Vocalizr service is not running on localhost:7860"
fi

# Check disk space
echo "💾 Checking disk space..."
AVAILABLE=$(df . | tail -1 | awk '{print $4}')
if [ "$AVAILABLE" -gt 2097152 ]; then  # 2GB in KB
    echo "✅ Sufficient disk space available"
else
    echo "⚠️  Low disk space (less than 2GB available)"
fi

# Check memory
echo "🧠 Checking memory usage..."
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
if [ "$MEMORY_USAGE" -lt 80 ]; then
    echo "✅ Memory usage OK (${MEMORY_USAGE}%)"
else
    echo "⚠️  High memory usage (${MEMORY_USAGE}%)"
fi

echo "✅ Health check complete"
```

## Installation Issues

### Python Version Incompatibility

**Problem**: Error about Python version requirement
```
ERROR: Python 3.12 or higher is required
```

**Solutions**:

1. **Check current Python version**:
   ```bash
   python --version
   python3 --version
   ```

2. **Install Python 3.12+ on Ubuntu/Debian**:
   ```bash
   sudo apt update
   sudo apt install software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt update
   sudo apt install python3.12 python3.12-pip python3.12-venv
   ```

3. **Install Python 3.12+ on macOS**:
   ```bash
   # Using Homebrew
   brew install python@3.12
   
   # Using pyenv
   pyenv install 3.12.0
   pyenv global 3.12.0
   ```

4. **Install Python 3.12+ on Windows**:
   - Download from [python.org](https://www.python.org/downloads/)
   - Or use Windows Store
   - Or use Chocolatey: `choco install python312`

### Package Installation Failures

**Problem**: pip install fails with dependency conflicts

**Solutions**:

1. **Use virtual environment**:
   ```bash
   python -m venv vocalizr-env
   source vocalizr-env/bin/activate  # Linux/macOS
   # or
   vocalizr-env\Scripts\activate     # Windows
   
   pip install --upgrade pip
   pip install vocalizr
   ```

2. **Clear pip cache**:
   ```bash
   pip cache purge
   pip install --no-cache-dir vocalizr
   ```

3. **Install with specific index**:
   ```bash
   pip install vocalizr --extra-index-url https://download.pytorch.org/whl/cu124
   ```

### uv Package Manager Issues

**Problem**: uv commands not working

**Solutions**:

1. **Install uv**:
   ```bash
   # Linux/macOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Using pip
   pip install uv
   ```

2. **Sync dependencies**:
   ```bash
   uv sync --refresh
   ```

## Runtime Issues

### Model Download Failures

**Problem**: Cannot download Kokoro model from Hugging Face

**Error Messages**:
```
LocalEntryNotFoundError: An error happened while trying to locate the file on the Hub
Failed to resolve 'huggingface.co'
```

**Solutions**:

1. **Check internet connectivity**:
   ```bash
   ping huggingface.co
   curl -I https://huggingface.co
   ```

2. **Set proxy if needed**:
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   export NO_PROXY=localhost,127.0.0.1
   ```

3. **Manual model download**:
   ```python
   import os
   os.environ['HF_HOME'] = '/path/to/cache'
   
   from huggingface_hub import snapshot_download
   snapshot_download(
       repo_id="hexgrad/Kokoro-82M",
       local_dir="/path/to/local/model"
   )
   ```

4. **Use offline mode** (after initial download):
   ```python
   os.environ['HF_HUB_OFFLINE'] = '1'
   ```

### Memory Errors

**Problem**: Out of memory errors during generation

**Error Messages**:
```
RuntimeError: CUDA out of memory
MemoryError: Unable to allocate array
```

**Solutions**:

1. **Reduce batch size**:
   ```python
   # Generate shorter texts
   text_chunks = [text[i:i+500] for i in range(0, len(text), 500)]
   ```

2. **Clear GPU memory**:
   ```python
   import torch
   torch.cuda.empty_cache()
   import gc
   gc.collect()
   ```

3. **Force CPU usage**:
   ```bash
   export CUDA_VISIBLE_DEVICES=""
   ```

4. **Increase system memory**:
   - Add swap space on Linux:
     ```bash
     sudo fallocate -l 4G /swapfile
     sudo chmod 600 /swapfile
     sudo mkswap /swapfile
     sudo swapon /swapfile
     ```

### Permission Errors

**Problem**: Cannot write to output directories

**Solutions**:

1. **Check directory permissions**:
   ```bash
   ls -la results/ logs/
   ```

2. **Fix permissions**:
   ```bash
   chmod 755 results/ logs/
   chown $USER:$USER results/ logs/
   ```

3. **Use custom directories**:
   ```bash
   export VOCALIZR_RESULTS_DIR=/tmp/vocalizr_results
   export VOCALIZR_LOG_DIR=/tmp/vocalizr_logs
   mkdir -p $VOCALIZR_RESULTS_DIR $VOCALIZR_LOG_DIR
   ```

## Performance Problems

### Slow Generation Times

**Problem**: Audio generation takes too long

**Diagnostics**:
```python
import time
import torch
from vocalizr.model import generate_audio_for_text

def benchmark_generation():
    text = "This is a performance test."
    
    # Check if CUDA is being used
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Current device: {torch.cuda.current_device()}")
        print(f"Device name: {torch.cuda.get_device_name()}")
    
    start_time = time.time()
    
    for sr, audio in generate_audio_for_text(text):
        break  # Just test first chunk
    
    end_time = time.time()
    print(f"Generation time: {end_time - start_time:.2f} seconds")

benchmark_generation()
```

**Solutions**:

1. **Enable GPU acceleration**:
   ```bash
   # Check GPU driver
   nvidia-smi
   
   # Install CUDA-enabled PyTorch
   pip install torch --index-url https://download.pytorch.org/whl/cu124
   ```

2. **Optimize system resources**:
   ```bash
   # Set CPU governor to performance
   echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
   
   # Disable CPU throttling
   echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
   ```

3. **Use caching**:
   ```python
   # Implement audio caching to avoid regeneration
   import hashlib
   import pickle
   
   def get_cache_key(text, voice, speed):
       return hashlib.md5(f"{text}{voice}{speed}".encode()).hexdigest()
   ```

### High Memory Usage

**Problem**: Application uses too much memory

**Solutions**:

1. **Monitor memory usage**:
   ```python
   import psutil
   import torch
   
   def monitor_memory():
       process = psutil.Process()
       memory_info = process.memory_info()
       print(f"RSS: {memory_info.rss / 1024**2:.1f} MB")
       
       if torch.cuda.is_available():
           print(f"GPU memory: {torch.cuda.memory_allocated() / 1024**2:.1f} MB")
   ```

2. **Implement memory cleanup**:
   ```python
   import gc
   
   def cleanup_memory():
       gc.collect()
       if torch.cuda.is_available():
           torch.cuda.empty_cache()
   ```

3. **Use memory-efficient settings**:
   ```python
   # Reduce model precision if supported
   torch.backends.cudnn.allow_tf32 = True
   torch.backends.cuda.matmul.allow_tf32 = True
   ```

## Network & Connectivity

### Port Already in Use

**Problem**: Cannot bind to port 7860

**Error Messages**:
```
OSError: [Errno 98] Address already in use
```

**Solutions**:

1. **Find process using port**:
   ```bash
   sudo lsof -i :7860
   sudo netstat -tulpn | grep :7860
   ```

2. **Kill process**:
   ```bash
   sudo kill -9 <PID>
   ```

3. **Use different port**:
   ```bash
   export GRADIO_SERVER_PORT=8080
   vocalizr
   ```

### Firewall Issues

**Problem**: Cannot access web interface externally

**Solutions**:

1. **Check firewall status**:
   ```bash
   # Ubuntu/Debian
   sudo ufw status
   
   # CentOS/RHEL
   sudo firewall-cmd --list-all
   ```

2. **Open port**:
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 7860
   
   # CentOS/RHEL
   sudo firewall-cmd --add-port=7860/tcp --permanent
   sudo firewall-cmd --reload
   ```

3. **Test connectivity**:
   ```bash
   # From another machine
   telnet your-server-ip 7860
   ```

### Proxy Configuration

**Problem**: Cannot access external services through corporate proxy

**Solutions**:

1. **Set proxy environment variables**:
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   export NO_PROXY=localhost,127.0.0.1,.company.com
   ```

2. **Configure pip proxy**:
   ```bash
   pip install --proxy http://proxy.company.com:8080 vocalizr
   ```

3. **Git proxy configuration**:
   ```bash
   git config --global http.proxy http://proxy.company.com:8080
   git config --global https.proxy http://proxy.company.com:8080
   ```

## Audio Generation Issues

### No Audio Output

**Problem**: Generation completes but no audio is produced

**Diagnostics**:
```python
def debug_audio_generation():
    from vocalizr.model import generate_audio_for_text
    import numpy as np
    
    text = "Hello world"
    
    for sr, audio in generate_audio_for_text(text, debug=True):
        print(f"Sample rate: {sr}")
        print(f"Audio shape: {audio.shape}")
        print(f"Audio dtype: {audio.dtype}")
        print(f"Audio range: [{audio.min():.3f}, {audio.max():.3f}]")
        print(f"Audio stats: mean={audio.mean():.3f}, std={audio.std():.3f}")
        
        # Check for silence
        if np.abs(audio).max() < 0.001:
            print("⚠️  Audio appears to be silent")
        break

debug_audio_generation()
```

**Solutions**:

1. **Check text input**:
   ```python
   # Ensure text is not empty or too short
   text = text.strip()
   if len(text) < 4:
       print("Text too short for generation")
   ```

2. **Verify voice selection**:
   ```python
   from vocalizr import CHOICES
   print("Available voices:", list(CHOICES.keys()))
   ```

3. **Test with simple text**:
   ```python
   # Use simple ASCII text first
   test_text = "This is a simple test."
   ```

### Distorted Audio

**Problem**: Generated audio sounds distorted or garbled

**Solutions**:

1. **Check sample rate**:
   ```python
   # Ensure correct sample rate when saving
   import soundfile as sf
   sf.write('output.wav', audio, 24000)  # Use correct sample rate
   ```

2. **Verify audio format**:
   ```python
   # Check audio data type and range
   audio = audio.astype(np.float32)
   audio = np.clip(audio, -1.0, 1.0)  # Ensure proper range
   ```

3. **Test different voices**:
   ```python
   # Some voices might work better for certain content
   for voice in ['af_heart', 'bf_emma', 'am_michael']:
       print(f"Testing voice: {voice}")
       # Generate and test
   ```

### Slow Audio Playback

**Problem**: Audio plays back too slowly or quickly

**Solutions**:

1. **Check speed parameter**:
   ```python
   # Ensure speed is reasonable
   speed = max(0.5, min(2.0, speed))  # Clamp to valid range
   ```

2. **Verify sample rate**:
   ```python
   # Use consistent sample rate
   EXPECTED_SAMPLE_RATE = 24000
   ```

## Docker & Container Issues

### Container Won't Start

**Problem**: Docker container fails to start

**Diagnostics**:
```bash
# Check container logs
docker logs vocalizr

# Check container status
docker ps -a

# Inspect container
docker inspect vocalizr
```

**Solutions**:

1. **Check resource limits**:
   ```bash
   # Increase memory limit
   docker run --memory=8g --cpus=4 vocalizr
   ```

2. **Verify environment variables**:
   ```bash
   docker run -e DEBUG=true vocalizr
   ```

3. **Check port mapping**:
   ```bash
   # Ensure port isn't already in use
   docker run -p 8080:7860 vocalizr
   ```

### Volume Mount Issues

**Problem**: Cannot access mounted volumes

**Solutions**:

1. **Check permissions**:
   ```bash
   # Ensure directories exist and have correct permissions
   mkdir -p ./cache ./results ./logs
   chmod 755 ./cache ./results ./logs
   ```

2. **Use absolute paths**:
   ```bash
   docker run -v $(pwd)/cache:/app/cache vocalizr
   ```

3. **SELinux issues** (CentOS/RHEL):
   ```bash
   # Add :Z flag for SELinux
   docker run -v $(pwd)/cache:/app/cache:Z vocalizr
   ```

## Deployment Issues

### Load Balancer Problems

**Problem**: Load balancer not distributing traffic correctly

**Solutions**:

1. **Check health endpoints**:
   ```bash
   curl http://localhost:7860/health
   ```

2. **Verify backend status**:
   ```bash
   # For HAProxy
   echo "show stat" | socat stdio /var/run/haproxy/admin.sock
   ```

3. **Test individual backends**:
   ```bash
   curl -H "Host: your-domain.com" http://backend1:7860/health
   ```

### SSL Certificate Issues

**Problem**: SSL/TLS certificate errors

**Solutions**:

1. **Check certificate validity**:
   ```bash
   openssl x509 -in cert.pem -text -noout
   openssl s_client -connect your-domain.com:443
   ```

2. **Verify certificate chain**:
   ```bash
   curl -I https://your-domain.com
   ```

3. **Test with curl**:
   ```bash
   curl -v https://your-domain.com/health
   ```

### Kubernetes Issues

**Problem**: Pods not starting or crashing

**Diagnostics**:
```bash
# Check pod status
kubectl get pods -n vocalizr

# Check pod logs
kubectl logs -f deployment/vocalizr -n vocalizr

# Describe pod for events
kubectl describe pod <pod-name> -n vocalizr

# Check resource usage
kubectl top pods -n vocalizr
```

**Solutions**:

1. **Check resource requests/limits**:
   ```yaml
   resources:
     requests:
       memory: "4Gi"
       cpu: "2"
     limits:
       memory: "8Gi"
       cpu: "4"
   ```

2. **Verify image pull**:
   ```bash
   kubectl describe pod <pod-name> -n vocalizr | grep -A 5 Events
   ```

3. **Check node resources**:
   ```bash
   kubectl describe nodes
   kubectl top nodes
   ```

## Development Issues

### IDE/Editor Problems

**Problem**: Code completion or linting not working

**Solutions**:

1. **VS Code configuration**:
   ```json
   {
     "python.defaultInterpreterPath": "./venv/bin/python",
     "python.linting.ruffEnabled": true
   }
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Rebuild language server cache**:
   - VS Code: Reload window (Ctrl+Shift+P > "Developer: Reload Window")
   - PyCharm: File > Invalidate Caches and Restart

### Testing Issues

**Problem**: Tests failing or not running

**Solutions**:

1. **Install test dependencies**:
   ```bash
   pip install pytest pytest-cov
   ```

2. **Run tests with verbose output**:
   ```bash
   pytest -v tests/
   ```

3. **Check test environment**:
   ```bash
   # Ensure test environment is isolated
   python -m pytest --tb=short
   ```

### Import Errors

**Problem**: Cannot import vocalizr modules

**Solutions**:

1. **Check installation**:
   ```bash
   pip show vocalizr
   python -c "import vocalizr; print(vocalizr.__file__)"
   ```

2. **Verify PYTHONPATH**:
   ```bash
   echo $PYTHONPATH
   python -c "import sys; print(sys.path)"
   ```

3. **Reinstall in development mode**:
   ```bash
   pip uninstall vocalizr
   pip install -e .
   ```

## Getting Help

### Log Collection

When reporting issues, collect these logs:

```bash
#!/bin/bash
# Collect diagnostic information

echo "Collecting Vocalizr diagnostic information..."

# Create output directory
mkdir -p vocalizr_diagnostics
cd vocalizr_diagnostics

# System information
echo "System Information:" > system_info.txt
uname -a >> system_info.txt
cat /etc/os-release >> system_info.txt 2>/dev/null || sw_vers >> system_info.txt 2>/dev/null
free -h >> system_info.txt 2>/dev/null || vm_stat >> system_info.txt 2>/dev/null

# Python environment
echo "Python Environment:" > python_info.txt
python --version >> python_info.txt
pip list >> python_info.txt

# GPU information
echo "GPU Information:" > gpu_info.txt
nvidia-smi >> gpu_info.txt 2>/dev/null || echo "No NVIDIA GPU detected" >> gpu_info.txt

# Docker information (if applicable)
if command -v docker &> /dev/null; then
    echo "Docker Information:" > docker_info.txt
    docker version >> docker_info.txt
    docker ps -a >> docker_info.txt
fi

# Application logs
if [ -d "../logs" ]; then
    cp -r ../logs/ ./
fi

# Create archive
cd ..
tar -czf vocalizr_diagnostics.tar.gz vocalizr_diagnostics/
echo "Diagnostic information saved to: vocalizr_diagnostics.tar.gz"
```

### Issue Reporting Template

When creating an issue, include:

```markdown
## Environment
- OS: [Ubuntu 22.04 / macOS 13.0 / Windows 11]
- Python version: [3.12.0]
- Vocalizr version: [0.0.1]
- Installation method: [pip / Docker / source]

## Description
Brief description of the issue.

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Error Messages
```
Paste any error messages here
```

## Additional Context
- Any relevant configuration
- Screenshots if applicable
- Related issues or discussions

## Diagnostic Information
Please attach the diagnostic bundle from the log collection script.
```

### Community Resources

- **GitHub Issues**: [https://github.com/AlphaSphereDotAI/vocalizr/issues](https://github.com/AlphaSphereDotAI/vocalizr/issues)
- **GitHub Discussions**: [https://github.com/AlphaSphereDotAI/vocalizr/discussions](https://github.com/AlphaSphereDotAI/vocalizr/discussions)
- **Email Support**: [mohamed.hisham.abdelzaher@gmail.com](mailto:mohamed.hisham.abdelzaher@gmail.com)

### Before Reporting Issues

1. **Search existing issues** for similar problems
2. **Try the latest version** to see if the issue is already fixed
3. **Run the diagnostic script** to gather system information
4. **Try minimal reproduction** to isolate the problem
5. **Check documentation** for configuration options

### Emergency Procedures

For critical production issues:

1. **Immediate mitigation**:
   - Switch to backup instances
   - Implement circuit breakers
   - Scale down if resource exhaustion

2. **Data collection**:
   - Capture logs before restart
   - Save memory dumps if needed
   - Document timeline of events

3. **Recovery**:
   - Restart services in safe mode
   - Gradually restore full functionality
   - Monitor for recurring issues

## Next Steps

- Review [Configuration Guide](CONFIGURATION.md) for optimization options
- Check [Deployment Guide](DEPLOYMENT.md) for production best practices
- See [Development Guide](DEVELOPMENT.md) for debugging techniques
- Visit [Examples](EXAMPLES.md) for working code samples