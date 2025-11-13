# 🎯 Usage Guide

Learn how to use Vocalizr effectively through its web interface, command line, and Python API.

## Table of Contents

- [Web Interface](#web-interface)
- [Command Line Interface](#command-line-interface)
- [Voice Selection](#voice-selection)
- [Configuration Options](#configuration-options)
- [File Management](#file-management)
- [Best Practices](#best-practices)

## Web Interface

The Gradio web interface provides an intuitive way to generate speech from text.

### Launching the Interface

```bash
# Start the application
uvx vocalizr

# Access at http://localhost:7860
```

### Interface Components

#### Text Input
- **Input Text Field**: Enter the text you want to convert to speech
- **Character Limit**: Set maximum characters to process (-1 for unlimited)

#### Voice Configuration
- **Voice Dropdown**: Select from 20+ available voices
- **Speed Slider**: Adjust playback speed (0.5x to 2.0x)

#### Hardware Settings
- **Hardware Display**: Shows current GPU/CPU status
- **Automatic Detection**: CUDA GPU automatically detected if available

#### Output Options
- **Save Audio File**: Enable to save generated audio as WAV file
- **Debug Mode**: Enable for detailed logging
- **Streaming Output**: Real-time audio generation and playback

#### Controls
- **Generate Button**: Start audio generation
- **Stop Button**: Cancel ongoing generation
- **Audio Player**: Play, pause, and download generated audio

### Step-by-Step Usage

1. **Enter Text**: Type or paste your text in the input field
2. **Select Voice**: Choose your preferred voice from the dropdown
3. **Adjust Settings**: Set speed, character limit, and other options
4. **Generate**: Click the "Generate" button
5. **Listen**: Audio will play automatically when ready
6. **Download**: Save audio file if needed

## Command Line Interface

### Basic Usage

```bash
# Start with default settings
vocalizr

# Custom port
GRADIO_SERVER_PORT=8080 vocalizr

# Debug mode
DEBUG=true vocalizr

# Custom server name (for external access)
GRADIO_SERVER_NAME=0.0.0.0 vocalizr
```

### Environment Variables

Set these before running `vocalizr`:

```bash
export GRADIO_SERVER_NAME=localhost  # Server host
export GRADIO_SERVER_PORT=7860       # Server port
export DEBUG=false                   # Debug mode
export HF_HOME=/path/to/cache       # Hugging Face cache directory
```

### Production Deployment

```bash
# Production settings
export GRADIO_SERVER_NAME=0.0.0.0
export GRADIO_SERVER_PORT=80
export DEBUG=false

vocalizr
```

## Voice Selection

Vocalizr offers a variety of voices with different characteristics:

### American Voices (Female)
- `af_heart` - Heart ❤️ (warm, friendly)
- `af_bella` - Bella 🔥 (energetic, vibrant)
- `af_nicole` - Nicole 🎧 (professional, clear)
- `af_aoede` - Aoede (melodic, smooth)
- `af_kore` - Kore (gentle, calm)
- `af_sarah` - Sarah (natural, conversational)
- `af_nova` - Nova (modern, crisp)
- `af_sky` - Sky (airy, light)
- `af_alloy` - Alloy (strong, confident)
- `af_jessica` - Jessica (friendly, approachable)
- `af_river` - River (flowing, dynamic)

### American Voices (Male)
- `am_michael` - Michael (authoritative, deep)
- `am_fenrir` - Fenrir (powerful, commanding)
- `am_puck` - Puck (playful, energetic)
- `am_echo` - Echo (resonant, clear)
- `am_eric` - Eric (professional, steady)
- `am_liam` - Liam (youthful, bright)
- `am_onyx` - Onyx (rich, smooth)
- `am_santa` - Santa (jolly, warm)
- `am_adam` - Adam (classic, reliable)

### British Voices
- `bf_emma` - Emma (female, elegant, refined)
- `bf_isabella` - Isabella (female, sophisticated)
- `bf_alice` - Alice (female, charming, proper)
- `bf_lily` - Lily (female, gentle, sweet)
- `bm_george` - George (male, distinguished)
- `bm_fable` - Fable (male, storytelling)
- `bm_lewis` - Lewis (male, intellectual)
- `bm_daniel` - Daniel (male, professional)

### Choosing the Right Voice

Consider these factors when selecting a voice:

- **Content Type**: Professional content vs. casual conversation
- **Audience**: Age group and preferences
- **Tone**: Formal, friendly, energetic, calm
- **Accent**: American vs. British English
- **Gender**: Male vs. female voice preference

## Configuration Options

### Speed Control
- **Range**: 0.5x to 2.0x
- **Default**: 1.0x (normal speed)
- **Use Cases**: 
  - 0.5x-0.8x: Learning, comprehension
  - 1.0x: Normal conversation
  - 1.2x-2.0x: Quick information delivery

### Character Limits
- **Default**: -1 (unlimited)
- **Recommended**: 500-1000 characters for optimal performance
- **Maximum**: Depends on available memory

### File Output
- **Format**: WAV (24kHz sample rate)
- **Location**: `results/` directory with timestamp
- **Naming**: `YYYY-MM-DD_HH-MM-SS.wav`

## File Management

### Output Structure
```
vocalizr/
├── results/           # Generated audio files
│   └── 2024-01-15_14-30-25.wav
├── logs/             # Application logs
│   └── 2024-01-15_14-30-25.log
└── cache/            # Model cache (automatic)
```

### Cleanup
```bash
# Remove old audio files (older than 7 days)
find results/ -name "*.wav" -mtime +7 -delete

# Clear logs
rm -rf logs/*.log

# Clear model cache (will re-download on next use)
rm -rf ~/.cache/huggingface/
```

## Best Practices

### Performance Optimization
1. **Use GPU**: Enable CUDA for faster generation
2. **Batch Processing**: Process multiple texts together
3. **Reasonable Length**: Keep texts under 1000 characters
4. **Cache Models**: Reuse the same voice for multiple generations

### Quality Guidelines
1. **Text Preparation**: Clean text of special characters
2. **Punctuation**: Use proper punctuation for natural pauses
3. **Voice Consistency**: Use the same voice for related content
4. **Speed Selection**: Choose appropriate speed for content type

### Resource Management
1. **Memory**: Monitor RAM usage with large texts
2. **Storage**: Regularly clean up generated files
3. **Network**: Ensure stable connection for model downloads
4. **Logs**: Monitor application logs for issues

### Production Tips
1. **Error Handling**: Implement retry logic for network issues
2. **Rate Limiting**: Limit concurrent generations
3. **Monitoring**: Track generation metrics
4. **Backup**: Save important generated audio files

## Troubleshooting

### Common Issues

#### Audio Quality Problems
- **Solution**: Try different voices or adjust speed
- **Check**: Text formatting and punctuation

#### Performance Issues
- **Solution**: Enable GPU acceleration
- **Check**: System memory and CPU usage

#### Generation Failures
- **Solution**: Reduce text length or character limit
- **Check**: Network connection and logs

For more troubleshooting help, see the [Troubleshooting Guide](TROUBLESHOOTING.md).

## Next Steps

- Explore the [API Documentation](API.md) for detailed technical reference
- Check [Examples](EXAMPLES.md) for real-world usage scenarios
- Review [Configuration](CONFIGURATION.md) for advanced customization
- See [Development Guide](DEVELOPMENT.md) for contributing to the project
