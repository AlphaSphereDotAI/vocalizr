# 🔧 API Documentation

Complete reference for Vocalizr's Python API and programmatic interfaces.

## Table of Contents

- [Core Functions](#core-functions)
- [Data Types](#data-types)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Web API](#web-api)
- [Integration Examples](#integration-examples)
- [Performance Considerations](#performance-considerations)

## Core Functions

### `generate_audio_for_text`

Main function for generating audio from text.

```python
def generate_audio_for_text(
    text: str,
    voice: str = "af_heart",
    speed: float = 1.0,
    save_file: bool = False,
    debug: bool = False,
    char_limit: int = -1,
) -> Generator[tuple[Literal[24000], ndarray[tuple[float32], dtype[float32]]], Any, None]
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | Required | Input text to convert to speech |
| `voice` | `str` | `"af_heart"` | Voice ID from available voices |
| `speed` | `float` | `1.0` | Playback speed multiplier (0.5-2.0) |
| `save_file` | `bool` | `False` | Whether to save audio to file |
| `debug` | `bool` | `False` | Enable debug logging |
| `char_limit` | `int` | `-1` | Character limit (-1 for unlimited) |

#### Returns

Generator yielding tuples of:
- `sample_rate` (int): Always 24000 Hz
- `audio_data` (numpy.ndarray): Audio samples as float32 array

#### Raises

- `Error`: Gradio error for invalid input or generation failure
- `RuntimeError`: File saving errors
- `ValueError`: Invalid parameter values

#### Example

```python
from vocalizr.model import generate_audio_for_text

# Basic usage
for sample_rate, audio in generate_audio_for_text("Hello World"):
    print(f"Generated {len(audio)} samples at {sample_rate} Hz")

# With all parameters
for sample_rate, audio in generate_audio_for_text(
    text="This is a longer text example.",
    voice="bf_emma",
    speed=1.2,
    save_file=True,
    debug=True,
    char_limit=100
):
    # Process audio data
    pass
```

### `save_file_wav`

Save audio array to WAV file.

```python
def save_file_wav(audio: ndarray[tuple[float32], dtype[float32]]) -> None
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `audio` | `numpy.ndarray` | Audio data as float32 array |

#### Raises

- `RuntimeError`: If file saving fails

#### Example

```python
from vocalizr.model import save_file_wav
import numpy as np

# Generate some audio data
for sample_rate, audio in generate_audio_for_text("Hello"):
    save_file_wav(audio)
    break
```

## Data Types

### Audio Data Format

Audio data is returned as NumPy arrays with the following specifications:

```python
# Type definition
AudioArray = ndarray[tuple[float32], dtype[float32]]

# Properties
sample_rate: int = 24000  # Fixed sample rate
dtype: numpy.dtype = numpy.float32  # Data type
channels: int = 1  # Mono audio
sample_range: tuple = (-1.0, 1.0)  # Normalized range
```

### Voice IDs

Complete list of available voice identifiers:

```python
# American Female Voices
AMERICAN_FEMALE = [
    "af_heart",    # Heart ❤️
    "af_bella",    # Bella 🔥
    "af_nicole",   # Nicole 🎧
    "af_aoede",    # Aoede
    "af_kore",     # Kore
    "af_sarah",    # Sarah
    "af_nova",     # Nova
    "af_sky",      # Sky
    "af_alloy",    # Alloy
    "af_jessica",  # Jessica
    "af_river",    # River
]

# American Male Voices
AMERICAN_MALE = [
    "am_michael",  # Michael
    "am_fenrir",   # Fenrir
    "am_puck",     # Puck
    "am_echo",     # Echo
    "am_eric",     # Eric
    "am_liam",     # Liam
    "am_onyx",     # Onyx
    "am_santa",    # Santa
    "am_adam",     # Adam
]

# British Female Voices
BRITISH_FEMALE = [
    "bf_emma",     # Emma
    "bf_isabella", # Isabella
    "bf_alice",    # Alice
    "bf_lily",     # Lily
]

# British Male Voices
BRITISH_MALE = [
    "bm_george",   # George
    "bm_fable",    # Fable
    "bm_lewis",    # Lewis
    "bm_daniel",   # Daniel
]
```

### Configuration Constants

Access to internal configuration:

```python
from vocalizr import (
    DEBUG,           # bool: Debug mode
    SERVER_NAME,     # str: Server hostname
    SERVER_PORT,     # int: Server port
    PIPELINE,        # KPipeline: Kokoro pipeline instance
    CURRENT_DATE,    # str: Current timestamp
    BASE_DIR,        # Path: Base directory
    RESULTS_DIR,     # Path: Results directory
    LOG_DIR,         # Path: Logs directory
    AUDIO_FILE_PATH, # Path: Output audio file path
    LOG_FILE_PATH,   # Path: Log file path
    CUDA_AVAILABLE,  # bool: CUDA availability
    CHOICES,         # dict: Voice choices mapping
)
```

## Configuration

### Environment Variables

Configure Vocalizr behavior through environment variables:

```python
import os

# Server configuration
os.environ['GRADIO_SERVER_NAME'] = 'localhost'
os.environ['GRADIO_SERVER_PORT'] = '7860'
os.environ['DEBUG'] = 'False'

# Hugging Face configuration
os.environ['HF_HOME'] = '/path/to/cache'
os.environ['HF_TOKEN'] = 'your_token_here'  # If needed

# CUDA configuration
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Specific GPU
```

### Runtime Configuration

Modify behavior programmatically:

```python
from vocalizr import PIPELINE

# Configure pipeline
PIPELINE.speed = 1.5  # Default speed
PIPELINE.device = 'cuda'  # Force device

# Check configuration
print(f"Pipeline device: {PIPELINE.device}")
print(f"Model repo: {PIPELINE.repo_id}")
```

## Error Handling

### Common Exceptions

```python
from gradio import Error
from huggingface_hub.errors import LocalEntryNotFoundError

try:
    for sr, audio in generate_audio_for_text("Hello"):
        pass
except Error as e:
    print(f"Gradio error: {e}")
except LocalEntryNotFoundError as e:
    print(f"Model not found: {e}")
except RuntimeError as e:
    print(f"Runtime error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Robust Generation Function

```python
import time
from typing import Optional

def robust_generate_audio(
    text: str,
    voice: str = "af_heart",
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> Optional[tuple[int, np.ndarray]]:
    """Generate audio with retry logic."""
    
    for attempt in range(max_retries):
        try:
            audio_chunks = []
            sample_rate = None
            
            for sr, audio in generate_audio_for_text(
                text=text, 
                voice=voice
            ):
                if sample_rate is None:
                    sample_rate = sr
                audio_chunks.append(audio)
            
            if audio_chunks:
                full_audio = np.concatenate(audio_chunks)
                return sample_rate, full_audio
                
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
    
    return None
```

## Web API

### Gradio Interface Functions

Access Gradio app components:

```python
from vocalizr.gui import app_block

# Create Gradio app
app = app_block()

# Launch with custom settings
app.launch(
    server_name="0.0.0.0",
    server_port=8080,
    share=True,  # Create public link
    debug=True,
    auth=("username", "password"),  # Basic auth
    ssl_keyfile="path/to/key.pem",
    ssl_certfile="path/to/cert.pem"
)
```

### Custom Gradio Integration

```python
import gradio as gr
from vocalizr.model import generate_audio_for_text

def custom_tts_interface():
    """Create custom Gradio interface."""
    
    def process_text(text, voice, speed):
        try:
            audio_chunks = []
            sample_rate = None
            
            for sr, audio in generate_audio_for_text(
                text=text,
                voice=voice,
                speed=speed
            ):
                if sample_rate is None:
                    sample_rate = sr
                audio_chunks.append(audio)
            
            if audio_chunks:
                full_audio = np.concatenate(audio_chunks)
                return (sample_rate, full_audio)
            else:
                return None
                
        except Exception as e:
            gr.Warning(f"Generation failed: {e}")
            return None
    
    with gr.Blocks() as demo:
        gr.Markdown("# Custom Vocalizr Interface")
        
        with gr.Row():
            text_input = gr.Textbox(
                label="Text to Speech",
                placeholder="Enter your text here..."
            )
            voice_select = gr.Dropdown(
                choices=list(CHOICES.keys()),
                value="af_heart",
                label="Voice"
            )
            speed_slider = gr.Slider(
                minimum=0.5,
                maximum=2.0,
                value=1.0,
                step=0.1,
                label="Speed"
            )
        
        generate_btn = gr.Button("Generate Speech")
        audio_output = gr.Audio(label="Generated Audio")
        
        generate_btn.click(
            fn=process_text,
            inputs=[text_input, voice_select, speed_slider],
            outputs=audio_output
        )
    
    return demo

# Launch custom interface
if __name__ == "__main__":
    demo = custom_tts_interface()
    demo.launch()
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import tempfile
import soundfile as sf
import numpy as np

app = FastAPI(title="Vocalizr API")

@app.post("/generate-speech")
async def generate_speech(
    text: str,
    voice: str = "af_heart",
    speed: float = 1.0
):
    try:
        audio_chunks = []
        sample_rate = None
        
        for sr, audio in generate_audio_for_text(
            text=text,
            voice=voice,
            speed=speed
        ):
            if sample_rate is None:
                sample_rate = sr
            audio_chunks.append(audio)
        
        if not audio_chunks:
            raise HTTPException(400, "Failed to generate audio")
        
        full_audio = np.concatenate(audio_chunks)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(
            suffix='.wav', 
            delete=False
        ) as tmp:
            sf.write(tmp.name, full_audio, sample_rate)
            return FileResponse(
                tmp.name,
                media_type='audio/wav',
                filename=f'speech_{hash(text)}.wav'
            )
    
    except Exception as e:
        raise HTTPException(500, f"Generation error: {e}")

@app.get("/voices")
async def list_voices():
    return {"voices": list(CHOICES.keys())}
```

### Django Integration

```python
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import io
import soundfile as sf

@csrf_exempt
def text_to_speech(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text')
            voice = data.get('voice', 'af_heart')
            
            audio_chunks = []
            sample_rate = None
            
            for sr, audio in generate_audio_for_text(
                text=text,
                voice=voice
            ):
                if sample_rate is None:
                    sample_rate = sr
                audio_chunks.append(audio)
            
            if audio_chunks:
                full_audio = np.concatenate(audio_chunks)
                
                # Create in-memory WAV file
                buffer = io.BytesIO()
                sf.write(buffer, full_audio, sample_rate, format='WAV')
                buffer.seek(0)
                
                response = HttpResponse(
                    buffer.getvalue(),
                    content_type='audio/wav'
                )
                response['Content-Disposition'] = 'attachment; filename="speech.wav"'
                return response
            
            return JsonResponse({'error': 'Generation failed'}, status=500)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
```

### Streaming Integration

```python
import asyncio
from typing import AsyncGenerator

async def async_generate_audio(
    text: str,
    voice: str = "af_heart"
) -> AsyncGenerator[tuple[int, np.ndarray], None]:
    """Async wrapper for audio generation."""
    
    loop = asyncio.get_event_loop()
    
    # Run in thread pool to avoid blocking
    def sync_generate():
        return list(generate_audio_for_text(text=text, voice=voice))
    
    results = await loop.run_in_executor(None, sync_generate)
    
    for sample_rate, audio in results:
        yield sample_rate, audio

# Usage
async def main():
    async for sr, audio in async_generate_audio("Hello async world"):
        print(f"Received {len(audio)} samples")
```

## Performance Considerations

### Memory Management

```python
import gc
import torch

def memory_efficient_generation(texts, voice="af_heart"):
    """Generate audio with memory cleanup."""
    
    for text in texts:
        # Generate audio
        audio_chunks = []
        for sr, audio in generate_audio_for_text(text=text, voice=voice):
            audio_chunks.append(audio)
        
        # Process audio
        if audio_chunks:
            full_audio = np.concatenate(audio_chunks)
            yield sr, full_audio
        
        # Clean up
        del audio_chunks
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
```

### Batch Processing

```python
def batch_process_texts(
    texts: list[str],
    voice: str = "af_heart",
    batch_size: int = 5
):
    """Process texts in batches to manage memory."""
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        for text in batch:
            for sr, audio in generate_audio_for_text(
                text=text, 
                voice=voice
            ):
                yield text, sr, audio
        
        # Clean up between batches
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
```

### Caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_generate_audio(text_hash: str, voice: str, speed: float):
    """Cache audio generation results."""
    # Note: This is a simplified example
    # In practice, you'd need to handle the generator properly
    pass

def generate_with_cache(text: str, voice: str = "af_heart", speed: float = 1.0):
    """Generate audio with caching."""
    text_hash = hashlib.md5(text.encode()).hexdigest()
    
    # Try cache first
    try:
        return cached_generate_audio(text_hash, voice, speed)
    except:
        # Generate fresh
        return list(generate_audio_for_text(text=text, voice=voice, speed=speed))
```

## Next Steps

- Review [Configuration Guide](CONFIGURATION.md) for advanced settings
- Check [Examples](EXAMPLES.md) for practical implementations
- See [Development Guide](DEVELOPMENT.md) for contributing to the API
- Explore [Troubleshooting](TROUBLESHOOTING.md) for common API issues