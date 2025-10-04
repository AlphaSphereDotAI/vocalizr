# ⚙️ Configuration Guide

Comprehensive guide to configuring Vocalizr for different environments and use cases.

## Table of Contents

- [Environment Variables](#environment-variables)
- [Configuration Files](#configuration-files)
- [Runtime Configuration](#runtime-configuration)
- [Hardware Configuration](#hardware-configuration)
- [Deployment Configurations](#deployment-configurations)
- [Security Configuration](#security-configuration)
- [Logging Configuration](#logging-configuration)
- [Performance Tuning](#performance-tuning)

## Environment Variables

### Core Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `GRADIO_SERVER_NAME` | string | `localhost` | Server hostname/IP address |
| `GRADIO_SERVER_PORT` | integer | `7860` | Server port number |
| `DEBUG` | boolean | `True` | Enable debug mode |

### File Paths

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `HF_HOME` | string | `~/.cache/huggingface` | Hugging Face cache directory |
| `VOCALIZR_RESULTS_DIR` | string | `./results` | Audio output directory |
| `VOCALIZR_LOG_DIR` | string | `./logs` | Log file directory |

### Model Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VOCALIZR_MODEL_REPO` | string | `hexgrad/Kokoro-82M` | Hugging Face model repository |
| `VOCALIZR_LANG_CODE` | string | `a` | Language code for the model |
| `HF_TOKEN` | string | - | Hugging Face API token (if required) |

### Hardware Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CUDA_VISIBLE_DEVICES` | string | - | Specific GPU devices to use |
| `TORCH_DEVICE` | string | `auto` | PyTorch device (cpu/cuda/auto) |

### Examples

#### Development Environment

```bash
# .env file for development
GRADIO_SERVER_NAME=localhost
GRADIO_SERVER_PORT=7860
DEBUG=true
HF_HOME=/tmp/huggingface_cache
VOCALIZR_RESULTS_DIR=./dev_results
VOCALIZR_LOG_DIR=./dev_logs
```

#### Production Environment

```bash
# .env file for production
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=80
DEBUG=false
HF_HOME=/app/cache
VOCALIZR_RESULTS_DIR=/app/results
VOCALIZR_LOG_DIR=/app/logs
HF_TOKEN=your_production_token
```

#### Docker Environment

```bash
# Docker environment variables
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
HF_HOME=/home/nonroot/hf
DEBUG=false
```

## Configuration Files

### .env File

Create a `.env` file in your project root:

```bash
# Server Configuration
GRADIO_SERVER_NAME=localhost
GRADIO_SERVER_PORT=7860
DEBUG=false

# Model Configuration
VOCALIZR_MODEL_REPO=hexgrad/Kokoro-82M
VOCALIZR_LANG_CODE=a

# File Paths
HF_HOME=/path/to/cache
VOCALIZR_RESULTS_DIR=/path/to/results
VOCALIZR_LOG_DIR=/path/to/logs

# Authentication (if needed)
HF_TOKEN=your_huggingface_token

# Hardware
CUDA_VISIBLE_DEVICES=0,1
```

### Python Configuration

Create a `config.py` file:

```python
import os
from pathlib import Path

class VocalizrConfig:
    """Vocalizr configuration class."""
    
    # Server settings
    SERVER_NAME = os.getenv('GRADIO_SERVER_NAME', 'localhost')
    SERVER_PORT = int(os.getenv('GRADIO_SERVER_PORT', '7860'))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Model settings
    MODEL_REPO = os.getenv('VOCALIZR_MODEL_REPO', 'hexgrad/Kokoro-82M')
    LANG_CODE = os.getenv('VOCALIZR_LANG_CODE', 'a')
    
    # Paths
    BASE_DIR = Path.cwd()
    RESULTS_DIR = Path(os.getenv('VOCALIZR_RESULTS_DIR', BASE_DIR / 'results'))
    LOG_DIR = Path(os.getenv('VOCALIZR_LOG_DIR', BASE_DIR / 'logs'))
    HF_HOME = Path(os.getenv('HF_HOME', Path.home() / '.cache' / 'huggingface'))
    
    # Authentication
    HF_TOKEN = os.getenv('HF_TOKEN')
    
    # Hardware
    CUDA_DEVICES = os.getenv('CUDA_VISIBLE_DEVICES')
    TORCH_DEVICE = os.getenv('TORCH_DEVICE', 'auto')
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories."""
        cls.RESULTS_DIR.mkdir(exist_ok=True)
        cls.LOG_DIR.mkdir(exist_ok=True)
        cls.HF_HOME.mkdir(parents=True, exist_ok=True)

# Usage
config = VocalizrConfig()
config.create_directories()
```

### YAML Configuration

Create a `config.yaml` file:

```yaml
# Vocalizr Configuration

server:
  name: localhost
  port: 7860
  debug: true

model:
  repository: hexgrad/Kokoro-82M
  language_code: a
  cache_dir: ~/.cache/huggingface

paths:
  results: ./results
  logs: ./logs
  cache: ~/.cache/vocalizr

hardware:
  use_cuda: auto
  visible_devices: null
  device: auto

logging:
  level: INFO
  format: "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
  colorize: true
  file_rotation: "1 day"
  file_retention: "7 days"

performance:
  max_concurrent_generations: 5
  memory_limit: 8GB
  timeout: 300

security:
  enable_auth: false
  username: null
  password: null
  ssl_enabled: false
  ssl_cert: null
  ssl_key: null
```

Load YAML configuration:

```python
import yaml
from pathlib import Path

def load_yaml_config(config_path="config.yaml"):
    """Load configuration from YAML file."""
    config_file = Path(config_path)
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    else:
        raise FileNotFoundError(f"Configuration file {config_path} not found")

# Usage
config = load_yaml_config()
server_port = config['server']['port']
```

## Runtime Configuration

### Programmatic Configuration

```python
import os
from vocalizr import PIPELINE

def configure_vocalizr():
    """Configure Vocalizr at runtime."""
    
    # Modify environment variables
    os.environ['DEBUG'] = 'false'
    os.environ['GRADIO_SERVER_PORT'] = '8080'
    
    # Configure pipeline
    PIPELINE.speed = 1.2  # Default speed
    PIPELINE.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Set up logging
    from loguru import logger
    logger.remove()  # Remove default handler
    logger.add(
        "./logs/vocalizr.log",
        rotation="1 day",
        retention="1 week",
        level="INFO"
    )

configure_vocalizr()
```

### Dynamic Configuration

```python
class DynamicConfig:
    """Dynamic configuration that can be updated at runtime."""
    
    def __init__(self):
        self._config = {
            'default_voice': 'af_heart',
            'default_speed': 1.0,
            'max_text_length': 1000,
            'auto_save': False,
            'debug_mode': False
        }
    
    def get(self, key, default=None):
        return self._config.get(key, default)
    
    def set(self, key, value):
        self._config[key] = value
        print(f"Configuration updated: {key} = {value}")
    
    def update(self, **kwargs):
        self._config.update(kwargs)
        print(f"Configuration updated: {kwargs}")
    
    def reset(self):
        """Reset to default configuration."""
        self.__init__()

# Global configuration instance
config = DynamicConfig()

# Usage
config.set('default_voice', 'bf_emma')
config.update(default_speed=1.5, auto_save=True)
```

## Hardware Configuration

### GPU Configuration

```bash
# Use specific GPU devices
export CUDA_VISIBLE_DEVICES=0,1

# Force CPU usage
export CUDA_VISIBLE_DEVICES=""

# Set GPU memory fraction
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

Python GPU configuration:

```python
import torch
import os

def configure_gpu():
    """Configure GPU settings."""
    
    if torch.cuda.is_available():
        # Set memory allocation strategy
        torch.cuda.set_per_process_memory_fraction(0.8)
        
        # Enable memory mapping for large models
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        
        # Print GPU info
        print(f"CUDA devices available: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            print(f"Device {i}: {props.name} ({props.total_memory // 1024**2} MB)")
    
    else:
        print("CUDA not available, using CPU")

configure_gpu()
```

### Memory Configuration

```python
import psutil
import gc

def configure_memory():
    """Configure memory settings."""
    
    # Get system memory info
    memory = psutil.virtual_memory()
    available_gb = memory.available / (1024**3)
    
    print(f"Available memory: {available_gb:.1f} GB")
    
    # Configure based on available memory
    if available_gb < 4:
        print("Low memory detected, using conservative settings")
        os.environ['VOCALIZR_MAX_CONCURRENT'] = '1'
        os.environ['VOCALIZR_BATCH_SIZE'] = '1'
    elif available_gb < 8:
        print("Medium memory detected, using balanced settings")
        os.environ['VOCALIZR_MAX_CONCURRENT'] = '3'
        os.environ['VOCALIZR_BATCH_SIZE'] = '2'
    else:
        print("High memory detected, using optimal settings")
        os.environ['VOCALIZR_MAX_CONCURRENT'] = '5'
        os.environ['VOCALIZR_BATCH_SIZE'] = '4'
    
    # Enable aggressive garbage collection
    gc.set_threshold(700, 10, 10)

configure_memory()
```

## Deployment Configurations

### Docker Configuration

#### Dockerfile Configuration

```dockerfile
# Set environment variables
ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    HF_HOME=/home/nonroot/hf \
    DEBUG=false \
    PYTHONUNBUFFERED=1

# Configure cache directory
RUN mkdir -p /home/nonroot/hf && \
    chown -R nonroot:nonroot /home/nonroot/hf
```

#### Docker Compose Configuration

```yaml
version: '3.8'

services:
  vocalizr:
    image: ghcr.io/alphaspheredotai/vocalizr:latest
    container_name: vocalizr
    ports:
      - "7860:7860"
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - GRADIO_SERVER_PORT=7860
      - DEBUG=false
      - HF_HOME=/app/cache
    volumes:
      - ./cache:/app/cache
      - ./results:/app/results
      - ./logs:/app/logs
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '4.0'
        reservations:
          memory: 4G
          cpus: '2.0'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # Optional: Redis for caching
  redis:
    image: redis:alpine
    container_name: vocalizr-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### Kubernetes Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vocalizr
  labels:
    app: vocalizr
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vocalizr
  template:
    metadata:
      labels:
        app: vocalizr
    spec:
      containers:
      - name: vocalizr
        image: ghcr.io/alphaspheredotai/vocalizr:latest
        ports:
        - containerPort: 7860
        env:
        - name: GRADIO_SERVER_NAME
          value: "0.0.0.0"
        - name: GRADIO_SERVER_PORT
          value: "7860"
        - name: DEBUG
          value: "false"
        - name: HF_HOME
          value: "/app/cache"
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        volumeMounts:
        - name: cache-volume
          mountPath: /app/cache
        - name: results-volume
          mountPath: /app/results
        livenessProbe:
          httpGet:
            path: /health
            port: 7860
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 7860
          initialDelaySeconds: 30
          periodSeconds: 10
      volumes:
      - name: cache-volume
        persistentVolumeClaim:
          claimName: vocalizr-cache-pvc
      - name: results-volume
        persistentVolumeClaim:
          claimName: vocalizr-results-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: vocalizr-service
spec:
  selector:
    app: vocalizr
  ports:
  - protocol: TCP
    port: 80
    targetPort: 7860
  type: LoadBalancer
```

## Security Configuration

### Authentication

```python
def setup_authentication():
    """Configure authentication for Gradio app."""
    
    import gradio as gr
    from vocalizr.gui import app_block
    
    # Basic authentication
    auth = None
    if os.getenv('VOCALIZR_AUTH_ENABLED', 'false').lower() == 'true':
        username = os.getenv('VOCALIZR_USERNAME')
        password = os.getenv('VOCALIZR_PASSWORD')
        if username and password:
            auth = (username, password)
    
    # SSL configuration
    ssl_keyfile = os.getenv('VOCALIZR_SSL_KEY')
    ssl_certfile = os.getenv('VOCALIZR_SSL_CERT')
    
    app = app_block()
    app.launch(
        auth=auth,
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile,
        share=False,  # Don't create public links
        enable_queue=True
    )
```

### Rate Limiting

```python
import time
from collections import defaultdict
from functools import wraps

class RateLimiter:
    def __init__(self, max_requests=10, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id):
        now = time.time()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.time_window
        ]
        
        # Check if under limit
        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(now)
            return True
        
        return False

rate_limiter = RateLimiter(max_requests=10, time_window=60)

def rate_limit_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        client_id = kwargs.get('client_id', 'default')
        
        if not rate_limiter.is_allowed(client_id):
            raise Exception("Rate limit exceeded")
        
        return func(*args, **kwargs)
    
    return wrapper
```

## Logging Configuration

### Advanced Logging Setup

```python
from loguru import logger
import sys
import os

def setup_logging():
    """Configure comprehensive logging."""
    
    # Remove default handler
    logger.remove()
    
    # Console handler (for development)
    if os.getenv('DEBUG', 'false').lower() == 'true':
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
                   "<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG",
            colorize=True
        )
    
    # File handler (for production)
    log_dir = os.getenv('VOCALIZR_LOG_DIR', './logs')
    logger.add(
        f"{log_dir}/vocalizr.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
               "{name}:{function}:{line} - {message}",
        level="INFO",
        rotation="10 MB",
        retention="1 month",
        compression="gz"
    )
    
    # Error handler (separate file for errors)
    logger.add(
        f"{log_dir}/errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
               "{name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="5 MB",
        retention="3 months"
    )
    
    # Performance monitoring
    if os.getenv('VOCALIZR_PERF_LOGGING', 'false').lower() == 'true':
        logger.add(
            f"{log_dir}/performance.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
            filter=lambda record: "PERF" in record["extra"],
            rotation="1 day",
            retention="1 week"
        )

setup_logging()
```

### Structured Logging

```python
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self):
        self.logger = logger
    
    def log_generation(self, text, voice, duration, success=True, error=None):
        """Log audio generation events."""
        log_data = {
            "event": "audio_generation",
            "timestamp": datetime.utcnow().isoformat(),
            "text_length": len(text),
            "voice": voice,
            "duration_seconds": duration,
            "success": success,
            "error": str(error) if error else None
        }
        
        if success:
            self.logger.info(f"GENERATION_SUCCESS: {json.dumps(log_data)}")
        else:
            self.logger.error(f"GENERATION_FAILED: {json.dumps(log_data)}")
    
    def log_performance(self, metric_name, value, unit="seconds"):
        """Log performance metrics."""
        log_data = {
            "event": "performance_metric",
            "timestamp": datetime.utcnow().isoformat(),
            "metric": metric_name,
            "value": value,
            "unit": unit
        }
        
        self.logger.bind(PERF=True).info(json.dumps(log_data))

# Usage
structured_logger = StructuredLogger()
```

## Performance Tuning

### Memory Optimization

```python
import gc
import torch
from functools import wraps

def memory_monitor(func):
    """Decorator to monitor memory usage."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
            start_memory = torch.cuda.memory_allocated()
        
        result = func(*args, **kwargs)
        
        if torch.cuda.is_available():
            end_memory = torch.cuda.memory_allocated()
            peak_memory = torch.cuda.max_memory_allocated()
            print(f"Memory used: {(end_memory - start_memory) / 1024**2:.1f} MB")
            print(f"Peak memory: {peak_memory / 1024**2:.1f} MB")
        
        return result
    
    return wrapper

def optimize_memory():
    """Optimize memory settings."""
    
    # Enable memory-efficient attention
    if torch.cuda.is_available():
        torch.backends.cuda.enable_flash_sdp(True)
    
    # Set garbage collection thresholds
    gc.set_threshold(700, 10, 10)
    
    # Configure PyTorch memory allocation
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.set_per_process_memory_fraction(0.8)
```

### Concurrent Processing

```python
import asyncio
import concurrent.futures
from typing import List, Tuple

class ConcurrentProcessor:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_batch(self, texts: List[str], voice: str = "af_heart"):
        """Process multiple texts concurrently."""
        loop = asyncio.get_event_loop()
        
        # Create tasks for each text
        tasks = []
        for text in texts:
            task = loop.run_in_executor(
                self.executor,
                self._generate_sync,
                text,
                voice
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    def _generate_sync(self, text: str, voice: str):
        """Synchronous generation for thread executor."""
        audio_chunks = []
        for sr, audio in generate_audio_for_text(text=text, voice=voice):
            audio_chunks.append((sr, audio))
        return audio_chunks

# Usage
processor = ConcurrentProcessor(max_workers=4)
results = asyncio.run(processor.process_batch(["Hello", "World", "Test"]))
```

### Configuration Validation

```python
import os
from typing import Any, Dict

class ConfigValidator:
    """Validate configuration settings."""
    
    REQUIRED_VARS = ['GRADIO_SERVER_NAME', 'GRADIO_SERVER_PORT']
    TYPE_MAPPING = {
        'GRADIO_SERVER_PORT': int,
        'DEBUG': lambda x: x.lower() == 'true'
    }
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """Validate current configuration."""
        errors = []
        config = {}
        
        # Check required variables
        for var in cls.REQUIRED_VARS:
            value = os.getenv(var)
            if value is None:
                errors.append(f"Required environment variable {var} not set")
            else:
                # Type conversion
                if var in cls.TYPE_MAPPING:
                    try:
                        value = cls.TYPE_MAPPING[var](value)
                    except (ValueError, TypeError) as e:
                        errors.append(f"Invalid type for {var}: {e}")
                
                config[var] = value
        
        # Additional validation
        port = config.get('GRADIO_SERVER_PORT')
        if port and (port < 1 or port > 65535):
            errors.append(f"Invalid port number: {port}")
        
        if errors:
            raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
        
        return config

# Validate configuration on startup
try:
    validated_config = ConfigValidator.validate()
    print("Configuration validation passed")
except ValueError as e:
    print(f"Configuration error: {e}")
    exit(1)
```

## Next Steps

- Review [Development Guide](DEVELOPMENT.md) for development-specific configuration
- Check [Deployment Guide](DEPLOYMENT.md) for production deployment settings
- See [Troubleshooting](TROUBLESHOOTING.md) for configuration-related issues
- Explore [API Documentation](API.md) for programmatic configuration options