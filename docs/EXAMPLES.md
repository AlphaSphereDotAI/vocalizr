# 📚 Examples and Tutorials

Practical examples and tutorials for using Vocalizr in various scenarios.

## Table of Contents

- [Basic Examples](#basic-examples)
- [Advanced Use Cases](#advanced-use-cases)
- [Integration Examples](#integration-examples)
- [Automation Scripts](#automation-scripts)
- [Production Examples](#production-examples)
- [Creative Applications](#creative-applications)

## Basic Examples

### Simple Text-to-Speech

```python
from vocalizr.model import generate_audio_for_text

# Basic usage
text = "Hello, welcome to Vocalizr!"

for sample_rate, audio in generate_audio_for_text(text):
    print(f"Generated {len(audio)} audio samples at {sample_rate}Hz")
    break  # Just get the first chunk
```

### Save Audio to File

```python
import numpy as np
import soundfile as sf
from vocalizr.model import generate_audio_for_text

def text_to_file(text, filename, voice="af_heart", speed=1.0):
    """Convert text to speech and save to file."""
    
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
        sf.write(filename, full_audio, sample_rate)
        print(f"Audio saved to {filename}")
        return filename
    else:
        print("Failed to generate audio")
        return None

# Usage
text_to_file(
    "This is a test of the Vocalizr text-to-speech system.",
    "test_output.wav",
    voice="bf_emma",
    speed=1.2
)
```

### Voice Comparison

```python
from vocalizr.model import generate_audio_for_text
import soundfile as sf

def compare_voices(text, voices, output_dir="voice_comparison"):
    """Generate the same text with different voices for comparison."""
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    for voice_id in voices:
        print(f"Generating with voice: {voice_id}")
        
        audio_chunks = []
        sample_rate = None
        
        for sr, audio in generate_audio_for_text(text=text, voice=voice_id):
            if sample_rate is None:
                sample_rate = sr
            audio_chunks.append(audio)
        
        if audio_chunks:
            full_audio = np.concatenate(audio_chunks)
            filename = f"{output_dir}/{voice_id}_sample.wav"
            sf.write(filename, full_audio, sample_rate)
            results[voice_id] = filename
            print(f"Saved: {filename}")
    
    return results

# Compare different voices
sample_text = "The quick brown fox jumps over the lazy dog."
voice_list = ["af_heart", "bf_emma", "am_michael", "bm_george"]

comparison_files = compare_voices(sample_text, voice_list)
print("Generated files:", comparison_files)
```

## Advanced Use Cases

### Batch Processing

```python
import os
import json
from pathlib import Path
from vocalizr.model import generate_audio_for_text
import soundfile as sf

class BatchProcessor:
    """Process multiple texts efficiently."""
    
    def __init__(self, output_dir="batch_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
    
    def process_file(self, input_file, voice="af_heart", speed=1.0):
        """Process a text file line by line."""
        
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            print(f"Processing line {i+1}/{len(lines)}: {line[:50]}...")
            
            # Generate audio
            audio_chunks = []
            sample_rate = None
            
            for sr, audio in generate_audio_for_text(
                text=line,
                voice=voice,
                speed=speed
            ):
                if sample_rate is None:
                    sample_rate = sr
                audio_chunks.append(audio)
            
            if audio_chunks:
                full_audio = np.concatenate(audio_chunks)
                filename = self.output_dir / f"line_{i+1:03d}.wav"
                sf.write(filename, full_audio, sample_rate)
                
                self.results.append({
                    "line_number": i + 1,
                    "text": line,
                    "filename": str(filename),
                    "voice": voice,
                    "speed": speed
                })
        
        return self.results
    
    def process_json(self, json_file):
        """Process a JSON file with structured data."""
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            text = item.get('text', '')
            voice = item.get('voice', 'af_heart')
            speed = item.get('speed', 1.0)
            output_name = item.get('output_name', f"item_{len(self.results)+1}")
            
            if not text:
                continue
            
            print(f"Processing: {output_name}")
            
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
                filename = self.output_dir / f"{output_name}.wav"
                sf.write(filename, full_audio, sample_rate)
                
                self.results.append({
                    "name": output_name,
                    "text": text,
                    "filename": str(filename),
                    "voice": voice,
                    "speed": speed
                })
        
        return self.results
    
    def save_manifest(self, filename="manifest.json"):
        """Save processing results to a manifest file."""
        manifest_path = self.output_dir / filename
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"Manifest saved to {manifest_path}")
        return manifest_path

# Usage examples

# Process a text file
processor = BatchProcessor("my_batch_output")
processor.process_file("input_texts.txt", voice="bf_emma", speed=1.1)
processor.save_manifest()

# Process structured JSON data
json_data = [
    {
        "text": "Welcome to our service",
        "voice": "af_heart",
        "speed": 1.0,
        "output_name": "welcome_message"
    },
    {
        "text": "Thank you for your purchase",
        "voice": "bf_emma", 
        "speed": 0.9,
        "output_name": "thank_you_message"
    }
]

with open("input_data.json", "w") as f:
    json.dump(json_data, f)

processor.process_json("input_data.json")
```

### Audio Book Generator

```python
import re
from pathlib import Path
from vocalizr.model import generate_audio_for_text
import soundfile as sf

class AudioBookGenerator:
    """Generate an audiobook from text chapters."""
    
    def __init__(self, output_dir="audiobook"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.chapters = []
    
    def split_into_chapters(self, text_file):
        """Split a book into chapters."""
        
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by chapter markers (customize as needed)
        chapter_pattern = r'(Chapter \d+|CHAPTER \d+|Chapter [IVX]+)'
        chapters = re.split(chapter_pattern, content)
        
        # Combine headers with content
        chapter_list = []
        for i in range(1, len(chapters), 2):
            if i + 1 < len(chapters):
                header = chapters[i].strip()
                content = chapters[i + 1].strip()
                if content:
                    chapter_list.append({
                        'title': header,
                        'content': content[:5000]  # Limit length for demo
                    })
        
        self.chapters = chapter_list
        return chapter_list
    
    def generate_chapter(self, chapter_data, voice="af_heart", speed=1.0):
        """Generate audio for a single chapter."""
        
        title = chapter_data['title']
        content = chapter_data['content']
        
        # Combine title and content
        full_text = f"{title}. {content}"
        
        print(f"Generating audio for: {title}")
        
        audio_chunks = []
        sample_rate = None
        
        for sr, audio in generate_audio_for_text(
            text=full_text,
            voice=voice,
            speed=speed
        ):
            if sample_rate is None:
                sample_rate = sr
            audio_chunks.append(audio)
        
        if audio_chunks:
            full_audio = np.concatenate(audio_chunks)
            
            # Safe filename
            safe_title = re.sub(r'[^\w\s-]', '', title).strip()
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = self.output_dir / f"{safe_title}.wav"
            
            sf.write(filename, full_audio, sample_rate)
            print(f"Chapter saved: {filename}")
            return filename
        
        return None
    
    def generate_full_book(self, voice="af_heart", speed=1.0):
        """Generate audio for all chapters."""
        
        results = []
        
        for i, chapter in enumerate(self.chapters):
            print(f"Processing chapter {i+1}/{len(self.chapters)}")
            filename = self.generate_chapter(chapter, voice, speed)
            
            if filename:
                results.append({
                    'chapter': i + 1,
                    'title': chapter['title'],
                    'filename': str(filename),
                    'voice': voice,
                    'speed': speed
                })
        
        return results

# Usage
book_generator = AudioBookGenerator("my_audiobook")

# Assuming you have a book file
# book_generator.split_into_chapters("book.txt")
# results = book_generator.generate_full_book(voice="bf_emma", speed=1.1)

# For demo, create sample chapters
sample_chapters = [
    {
        'title': 'Chapter 1: The Beginning',
        'content': 'This is the start of our story. It was a dark and stormy night...'
    },
    {
        'title': 'Chapter 2: The Adventure Continues', 
        'content': 'Our hero ventured forth into the unknown wilderness...'
    }
]

book_generator.chapters = sample_chapters
results = book_generator.generate_full_book(voice="af_heart", speed=1.0)
print("Generated audiobook chapters:", results)
```

## Integration Examples

### Flask Web API

```python
from flask import Flask, request, jsonify, send_file
from vocalizr.model import generate_audio_for_text
import tempfile
import numpy as np
import soundfile as sf
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "vocalizr-api"})

@app.route('/voices', methods=['GET'])
def list_voices():
    """List available voices."""
    from vocalizr import CHOICES
    
    voices = []
    for display_name, voice_id in CHOICES.items():
        # Parse display name for metadata
        parts = display_name.split(' ')
        flag = parts[0] if parts else ""
        gender = parts[1] if len(parts) > 1 else ""
        name = ' '.join(parts[2:]) if len(parts) > 2 else ""
        
        voices.append({
            "id": voice_id,
            "display_name": display_name,
            "name": name,
            "flag": flag,
            "gender": gender
        })
    
    return jsonify({"voices": voices})

@app.route('/generate', methods=['POST'])
def generate_speech():
    """Generate speech from text."""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'text' not in data:
            return jsonify({"error": "Text is required"}), 400
        
        text = data['text']
        voice = data.get('voice', 'af_heart')
        speed = float(data.get('speed', 1.0))
        format_type = data.get('format', 'wav')
        
        if not text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400
        
        # Generate audio
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
            return jsonify({"error": "Failed to generate audio"}), 500
        
        full_audio = np.concatenate(audio_chunks)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(
            suffix=f'.{format_type}', 
            delete=False
        ) as tmp:
            sf.write(tmp.name, full_audio, sample_rate)
            
            # Return file
            return send_file(
                tmp.name,
                mimetype=f'audio/{format_type}',
                as_attachment=True,
                download_name=f'speech_{hash(text)}.{format_type}',
                conditional=True
            )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-stream', methods=['POST'])
def generate_speech_stream():
    """Generate speech with streaming response."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        voice = data.get('voice', 'af_heart')
        speed = float(data.get('speed', 1.0))
        
        def generate():
            for sr, audio in generate_audio_for_text(
                text=text,
                voice=voice,
                speed=speed
            ):
                # Convert to bytes for streaming
                audio_bytes = audio.tobytes()
                yield audio_bytes
        
        return app.response_class(
            generate(),
            mimetype='audio/wav'
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Cleanup function
@app.teardown_request
def cleanup_temp_files(exception):
    """Clean up temporary files after request."""
    # In production, implement proper cleanup logic
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Discord Bot

```python
import discord
from discord.ext import commands
from vocalizr.model import generate_audio_for_text
import tempfile
import numpy as np
import soundfile as sf
import asyncio

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='speak')
async def text_to_speech(ctx, voice: str = 'af_heart', *, text: str):
    """Convert text to speech and send as audio file.
    
    Usage: !speak [voice] <text>
    Example: !speak af_heart Hello everyone!
    """
    
    if len(text) > 500:
        await ctx.send("Text too long! Please keep it under 500 characters.")
        return
    
    try:
        await ctx.send("Generating audio... 🔊")
        
        # Generate audio in a separate thread to avoid blocking
        loop = asyncio.get_event_loop()
        audio_data = await loop.run_in_executor(
            None, 
            generate_audio_sync, 
            text, 
            voice
        )
        
        if audio_data:
            sample_rate, audio = audio_data
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                sf.write(tmp.name, audio, sample_rate)
                
                # Send file to Discord
                with open(tmp.name, 'rb') as f:
                    file = discord.File(f, filename='speech.wav')
                    await ctx.send(
                        f"🎤 Speech generated with voice: {voice}",
                        file=file
                    )
            
            # Clean up
            import os
            os.unlink(tmp.name)
        else:
            await ctx.send("Failed to generate audio. Please try again.")
    
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

def generate_audio_sync(text, voice):
    """Synchronous wrapper for audio generation."""
    try:
        audio_chunks = []
        sample_rate = None
        
        for sr, audio in generate_audio_for_text(text=text, voice=voice):
            if sample_rate is None:
                sample_rate = sr
            audio_chunks.append(audio)
        
        if audio_chunks:
            full_audio = np.concatenate(audio_chunks)
            return sample_rate, full_audio
        
        return None
    except Exception:
        return None

@bot.command(name='voices')
async def list_voices(ctx):
    """List available voices."""
    from vocalizr import CHOICES
    
    voice_list = "\n".join([
        f"`{voice_id}` - {display_name}" 
        for display_name, voice_id in list(CHOICES.items())[:10]
    ])
    
    embed = discord.Embed(
        title="Available Voices",
        description=voice_list,
        color=0x00ff00
    )
    
    if len(CHOICES) > 10:
        embed.add_field(
            name="Note", 
            value=f"Showing 10 of {len(CHOICES)} voices. Use the voice ID with !speak",
            inline=False
        )
    
    await ctx.send(embed=embed)

# Run the bot
# bot.run('YOUR_BOT_TOKEN')
```

### Telegram Bot

```python
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from vocalizr.model import generate_audio_for_text
import tempfile
import numpy as np
import soundfile as sf

# Bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command."""
    await message.answer(
        "🔊 Welcome to Vocalizr Bot!\n\n"
        "Send me any text and I'll convert it to speech.\n"
        "Use /voices to see available voices.\n"
        "Use /speak <voice> <text> for specific voice."
    )

@dp.message(Command("voices"))
async def cmd_voices(message: types.Message):
    """List available voices."""
    from vocalizr import CHOICES
    
    voice_text = "🎭 Available voices:\n\n"
    for display_name, voice_id in list(CHOICES.items())[:15]:
        voice_text += f"• `{voice_id}` - {display_name}\n"
    
    if len(CHOICES) > 15:
        voice_text += f"\n... and {len(CHOICES) - 15} more voices"
    
    await message.answer(voice_text, parse_mode="Markdown")

@dp.message(Command("speak"))
async def cmd_speak(message: types.Message):
    """Handle /speak command with voice selection."""
    try:
        # Parse command: /speak voice_id text
        parts = message.text.split(' ', 2)
        if len(parts) < 3:
            await message.answer(
                "Usage: /speak <voice_id> <text>\n"
                "Example: /speak af_heart Hello world!"
            )
            return
        
        voice = parts[1]
        text = parts[2]
        
        await generate_and_send_audio(message, text, voice)
    
    except Exception as e:
        await message.answer(f"Error: {str(e)}")

@dp.message(F.text)
async def handle_text(message: types.Message):
    """Handle regular text messages."""
    if message.text.startswith('/'):
        return  # Skip commands
    
    await generate_and_send_audio(message, message.text)

async def generate_and_send_audio(message: types.Message, text: str, voice: str = "af_heart"):
    """Generate audio and send to user."""
    
    if len(text) > 1000:
        await message.answer("Text too long! Please keep it under 1000 characters.")
        return
    
    # Send "typing" action
    await bot.send_chat_action(message.chat.id, "upload_voice")
    
    try:
        # Generate audio
        loop = asyncio.get_event_loop()
        audio_data = await loop.run_in_executor(
            None,
            generate_audio_sync,
            text,
            voice
        )
        
        if audio_data:
            sample_rate, audio = audio_data
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as tmp:
                # Convert to OGG for better Telegram compatibility
                sf.write(tmp.name, audio, sample_rate, format='OGG')
                
                # Send voice message
                voice_file = types.FSInputFile(tmp.name)
                await message.answer_voice(voice_file)
            
            # Clean up
            import os
            os.unlink(tmp.name)
        
        else:
            await message.answer("Failed to generate audio. Please try again.")
    
    except Exception as e:
        await message.answer(f"Error generating audio: {str(e)}")

def generate_audio_sync(text, voice):
    """Synchronous wrapper for audio generation."""
    try:
        audio_chunks = []
        sample_rate = None
        
        for sr, audio in generate_audio_for_text(text=text, voice=voice):
            if sample_rate is None:
                sample_rate = sr
            audio_chunks.append(audio)
        
        if audio_chunks:
            full_audio = np.concatenate(audio_chunks)
            return sample_rate, full_audio
        
        return None
    except Exception:
        return None

async def main():
    """Main function to run the bot."""
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Automation Scripts

### Podcast Generator

```python
import json
import os
from pathlib import Path
from datetime import datetime
from vocalizr.model import generate_audio_for_text
import soundfile as sf

class PodcastGenerator:
    """Generate podcast episodes from scripts."""
    
    def __init__(self, output_dir="podcast_episodes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.episode_data = []
    
    def load_script(self, script_file):
        """Load a podcast script from JSON."""
        with open(script_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_episode(self, script_data):
        """Generate a complete podcast episode."""
        
        episode_title = script_data.get('title', 'Untitled Episode')
        segments = script_data.get('segments', [])
        
        print(f"Generating episode: {episode_title}")
        
        episode_audio = []
        episode_info = {
            'title': episode_title,
            'date': datetime.now().isoformat(),
            'segments': []
        }
        
        for i, segment in enumerate(segments):
            speaker = segment.get('speaker', 'Host')
            text = segment.get('text', '')
            voice = segment.get('voice', 'af_heart')
            pause_after = segment.get('pause_after', 0.5)
            
            if not text:
                continue
            
            print(f"  Segment {i+1}: {speaker}")
            
            # Generate audio for segment
            segment_audio = []
            sample_rate = None
            
            for sr, audio in generate_audio_for_text(text=text, voice=voice):
                if sample_rate is None:
                    sample_rate = sr
                segment_audio.append(audio)
            
            if segment_audio:
                full_segment = np.concatenate(segment_audio)
                episode_audio.append(full_segment)
                
                # Add pause
                if pause_after > 0:
                    silence = np.zeros(int(sample_rate * pause_after), dtype=np.float32)
                    episode_audio.append(silence)
                
                episode_info['segments'].append({
                    'speaker': speaker,
                    'text': text[:100] + '...' if len(text) > 100 else text,
                    'voice': voice,
                    'duration': len(full_segment) / sample_rate
                })
        
        # Combine all audio
        if episode_audio:
            full_episode = np.concatenate(episode_audio)
            
            # Safe filename
            safe_title = "".join(c for c in episode_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = self.output_dir / f"{safe_title}.wav"
            
            sf.write(filename, full_episode, sample_rate)
            episode_info['filename'] = str(filename)
            episode_info['duration'] = len(full_episode) / sample_rate
            
            self.episode_data.append(episode_info)
            print(f"Episode saved: {filename}")
            return episode_info
        
        return None

# Example podcast script
sample_script = {
    "title": "Tech Talk Episode 1",
    "description": "Introduction to AI and voice synthesis",
    "segments": [
        {
            "speaker": "Host",
            "text": "Welcome to Tech Talk, the podcast where we explore the latest in technology. I'm your host, and today we're diving into the world of artificial intelligence and voice synthesis.",
            "voice": "af_heart",
            "pause_after": 1.0
        },
        {
            "speaker": "Co-Host",
            "text": "That's right! Voice synthesis has come such a long way. Today we can generate incredibly natural-sounding speech from just text input.",
            "voice": "am_michael",
            "pause_after": 0.8
        },
        {
            "speaker": "Host",
            "text": "Absolutely! Tools like Vocalizr are making this technology accessible to everyone. Whether you're creating content, building applications, or just experimenting with AI, the possibilities are endless.",
            "voice": "af_heart",
            "pause_after": 1.5
        },
        {
            "speaker": "Co-Host", 
            "text": "And that's all for today's episode. Thanks for listening to Tech Talk, and we'll see you next time!",
            "voice": "am_michael",
            "pause_after": 0.5
        }
    ]
}

# Save sample script
with open("sample_podcast.json", "w") as f:
    json.dump(sample_script, f, indent=2)

# Generate podcast
generator = PodcastGenerator()
episode_info = generator.generate_episode(sample_script)
print("Generated episode:", episode_info)
```

### News Reader

```python
import requests
import json
from datetime import datetime
from vocalizr.model import generate_audio_for_text
import soundfile as sf

class NewsReader:
    """Convert news articles to audio."""
    
    def __init__(self, voice="af_heart", speed=1.0):
        self.voice = voice
        self.speed = speed
    
    def fetch_news(self, api_key, query="technology", language="en"):
        """Fetch news from NewsAPI (example)."""
        # This is a mock implementation
        # In practice, you'd use a real news API
        
        mock_articles = [
            {
                "title": "AI Technology Breakthrough",
                "description": "Scientists announce major advancement in artificial intelligence",
                "content": "Researchers have developed a new AI system that can understand and generate human-like speech with unprecedented accuracy..."
            },
            {
                "title": "Voice Synthesis Revolution", 
                "description": "New text-to-speech technology changes the game",
                "content": "A revolutionary new voice synthesis system is making it possible to generate natural-sounding speech from any text input..."
            }
        ]
        
        return mock_articles
    
    def create_news_summary(self, articles, max_articles=5):
        """Create a news summary script."""
        
        script = "Here's your daily news summary. "
        
        for i, article in enumerate(articles[:max_articles]):
            title = article.get('title', 'Untitled')
            description = article.get('description', '')
            
            script += f"Story {i+1}: {title}. "
            if description:
                script += f"{description} "
            script += "... "
        
        script += "That concludes today's news summary. Thank you for listening."
        
        return script
    
    def generate_news_audio(self, script, output_file="news_summary.wav"):
        """Generate audio from news script."""
        
        print("Generating news audio...")
        
        audio_chunks = []
        sample_rate = None
        
        for sr, audio in generate_audio_for_text(
            text=script,
            voice=self.voice,
            speed=self.speed
        ):
            if sample_rate is None:
                sample_rate = sr
            audio_chunks.append(audio)
        
        if audio_chunks:
            full_audio = np.concatenate(audio_chunks)
            sf.write(output_file, full_audio, sample_rate)
            print(f"News audio saved: {output_file}")
            return output_file
        
        return None
    
    def create_daily_briefing(self, api_key=None):
        """Create a complete daily news briefing."""
        
        # Fetch news
        articles = self.fetch_news(api_key)
        
        # Create script
        script = self.create_news_summary(articles)
        
        # Generate audio
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_file = f"daily_briefing_{timestamp}.wav"
        
        return self.generate_news_audio(script, output_file)

# Usage
reader = NewsReader(voice="bf_emma", speed=1.1)
briefing_file = reader.create_daily_briefing()
print(f"Daily briefing created: {briefing_file}")
```

## Production Examples

### Caching System

```python
import hashlib
import pickle
import os
from pathlib import Path
import time
from vocalizr.model import generate_audio_for_text

class AudioCache:
    """Cache system for generated audio."""
    
    def __init__(self, cache_dir="audio_cache", max_size_mb=1000):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_size_bytes = max_size_mb * 1024 * 1024
    
    def _get_cache_key(self, text, voice, speed):
        """Generate cache key from parameters."""
        key_string = f"{text}_{voice}_{speed}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key):
        """Get full path for cache file."""
        return self.cache_dir / f"{cache_key}.pkl"
    
    def get(self, text, voice, speed):
        """Get cached audio if available."""
        cache_key = self._get_cache_key(text, voice, speed)
        cache_path = self._get_cache_path(cache_key)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                
                # Update access time
                os.utime(cache_path)
                
                print(f"Cache hit for key: {cache_key}")
                return cached_data
            
            except Exception as e:
                print(f"Cache read error: {e}")
                # Remove corrupted cache file
                cache_path.unlink()
        
        return None
    
    def set(self, text, voice, speed, audio_data):
        """Cache audio data."""
        cache_key = self._get_cache_key(text, voice, speed)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(audio_data, f)
            
            print(f"Cached audio for key: {cache_key}")
            
            # Clean up if cache is too large
            self._cleanup_cache()
        
        except Exception as e:
            print(f"Cache write error: {e}")
    
    def _cleanup_cache(self):
        """Remove old cache files if cache is too large."""
        cache_files = list(self.cache_dir.glob("*.pkl"))
        
        # Calculate total size
        total_size = sum(f.stat().st_size for f in cache_files)
        
        if total_size > self.max_size_bytes:
            # Sort by access time (oldest first)
            cache_files.sort(key=lambda f: f.stat().st_atime)
            
            # Remove oldest files until under limit
            for cache_file in cache_files:
                cache_file.unlink()
                total_size -= cache_file.stat().st_size
                
                if total_size <= self.max_size_bytes * 0.8:  # Leave some headroom
                    break
            
            print("Cache cleanup completed")

class CachedVocalizr:
    """Vocalizr with caching support."""
    
    def __init__(self, cache_dir="audio_cache"):
        self.cache = AudioCache(cache_dir)
    
    def generate_audio_cached(self, text, voice="af_heart", speed=1.0):
        """Generate audio with caching."""
        
        # Try cache first
        cached_result = self.cache.get(text, voice, speed)
        if cached_result:
            return cached_result
        
        # Generate new audio
        print("Generating new audio...")
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
            result = (sample_rate, full_audio)
            
            # Cache the result
            self.cache.set(text, voice, speed, result)
            
            return result
        
        return None

# Usage
cached_vocalizr = CachedVocalizr()

# First call - generates and caches
result1 = cached_vocalizr.generate_audio_cached("Hello, this is a test message")

# Second call - returns from cache
result2 = cached_vocalizr.generate_audio_cached("Hello, this is a test message")
```

## Creative Applications

### Interactive Story Generator

```python
import random
from vocalizr.model import generate_audio_for_text
import soundfile as sf

class InteractiveStory:
    """Generate interactive audio stories."""
    
    def __init__(self):
        self.narrator_voice = "af_heart"
        self.character_voices = {
            "hero": "am_michael",
            "villain": "bm_george", 
            "sidekick": "af_bella",
            "wise_mentor": "bf_emma"
        }
        self.story_parts = []
    
    def create_story_template(self):
        """Create a branching story template."""
        return {
            "title": "The Adventure Begins",
            "scenes": [
                {
                    "id": "start",
                    "narrator": "Welcome, brave adventurer! You find yourself at the edge of a mysterious forest.",
                    "character": "hero",
                    "character_text": "I must choose my path carefully.",
                    "choices": [
                        {"text": "Enter the dark forest", "next": "forest"},
                        {"text": "Follow the mountain path", "next": "mountain"}
                    ]
                },
                {
                    "id": "forest",
                    "narrator": "You venture into the shadowy forest. Strange sounds echo around you.",
                    "character": "sidekick",
                    "character_text": "I sense danger nearby!",
                    "choices": [
                        {"text": "Investigate the sounds", "next": "encounter"},
                        {"text": "Turn back", "next": "start"}
                    ]
                },
                {
                    "id": "mountain",
                    "narrator": "The mountain path is steep but offers a beautiful view of the valley below.",
                    "character": "wise_mentor",
                    "character_text": "The high road often leads to wisdom.",
                    "choices": [
                        {"text": "Continue climbing", "next": "summit"},
                        {"text": "Rest and enjoy the view", "next": "rest"}
                    ]
                }
            ]
        }
    
    def generate_scene_audio(self, scene, output_dir="story_audio"):
        """Generate audio for a story scene."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        scene_id = scene["id"]
        audio_files = {}
        
        # Generate narrator audio
        if "narrator" in scene:
            narrator_audio = []
            sample_rate = None
            
            for sr, audio in generate_audio_for_text(
                text=scene["narrator"],
                voice=self.narrator_voice
            ):
                if sample_rate is None:
                    sample_rate = sr
                narrator_audio.append(audio)
            
            if narrator_audio:
                full_audio = np.concatenate(narrator_audio)
                narrator_file = f"{output_dir}/{scene_id}_narrator.wav"
                sf.write(narrator_file, full_audio, sample_rate)
                audio_files["narrator"] = narrator_file
        
        # Generate character audio
        if "character" in scene and "character_text" in scene:
            character = scene["character"]
            voice = self.character_voices.get(character, "af_heart")
            
            character_audio = []
            sample_rate = None
            
            for sr, audio in generate_audio_for_text(
                text=scene["character_text"],
                voice=voice
            ):
                if sample_rate is None:
                    sample_rate = sr
                character_audio.append(audio)
            
            if character_audio:
                full_audio = np.concatenate(character_audio)
                character_file = f"{output_dir}/{scene_id}_{character}.wav"
                sf.write(character_file, full_audio, sample_rate)
                audio_files["character"] = character_file
        
        return audio_files
    
    def create_choice_menu(self, choices):
        """Create audio for choice menu."""
        choice_text = "What would you like to do? Your options are: "
        
        for i, choice in enumerate(choices):
            choice_text += f"Option {i+1}: {choice['text']}. "
        
        choice_text += "Please make your selection."
        
        choice_audio = []
        sample_rate = None
        
        for sr, audio in generate_audio_for_text(
            text=choice_text,
            voice=self.narrator_voice,
            speed=0.9  # Slightly slower for clarity
        ):
            if sample_rate is None:
                sample_rate = sr
            choice_audio.append(audio)
        
        if choice_audio:
            return sample_rate, np.concatenate(choice_audio)
        
        return None

# Usage
story_generator = InteractiveStory()
story_template = story_generator.create_story_template()

print("Generating interactive story audio...")

for scene in story_template["scenes"]:
    print(f"Generating scene: {scene['id']}")
    
    # Generate scene audio
    audio_files = story_generator.generate_scene_audio(scene)
    print(f"Scene audio files: {audio_files}")
    
    # Generate choice menu
    if "choices" in scene:
        choice_audio = story_generator.create_choice_menu(scene["choices"])
        if choice_audio:
            sample_rate, audio = choice_audio
            choice_file = f"story_audio/{scene['id']}_choices.wav"
            sf.write(choice_file, audio, sample_rate)
            print(f"Choice menu: {choice_file}")

print("Interactive story generation complete!")
```

### Multilingual Content Creator

```python
from vocalizr.model import generate_audio_for_text
import soundfile as sf

class MultilingualContent:
    """Create content in multiple languages/accents."""
    
    def __init__(self):
        # Map languages to appropriate voices
        self.language_voices = {
            "american_english": ["af_heart", "am_michael"],
            "british_english": ["bf_emma", "bm_george"],
            "neutral": ["af_nicole", "am_eric"]
        }
    
    def create_multilingual_greeting(self, name="friend"):
        """Create greetings in different accents."""
        
        greetings = [
            {
                "text": f"Hello {name}, welcome to our international service!",
                "accent": "american_english",
                "label": "American English"
            },
            {
                "text": f"Good day {name}, lovely to have you with us!",
                "accent": "british_english", 
                "label": "British English"
            },
            {
                "text": f"Greetings {name}, thank you for joining us today!",
                "accent": "neutral",
                "label": "Neutral English"
            }
        ]
        
        results = {}
        
        for greeting in greetings:
            print(f"Generating {greeting['label']} greeting...")
            
            # Select appropriate voice
            voices = self.language_voices[greeting["accent"]]
            voice = voices[0]  # Use first available voice
            
            audio_chunks = []
            sample_rate = None
            
            for sr, audio in generate_audio_for_text(
                text=greeting["text"],
                voice=voice
            ):
                if sample_rate is None:
                    sample_rate = sr
                audio_chunks.append(audio)
            
            if audio_chunks:
                full_audio = np.concatenate(audio_chunks)
                filename = f"greeting_{greeting['accent']}.wav"
                sf.write(filename, full_audio, sample_rate)
                
                results[greeting["label"]] = {
                    "file": filename,
                    "text": greeting["text"],
                    "voice": voice
                }
        
        return results

# Usage
multilingual = MultilingualContent()
greetings = multilingual.create_multilingual_greeting("Alex")

print("Generated multilingual greetings:")
for label, info in greetings.items():
    print(f"  {label}: {info['file']} (using {info['voice']})")
```

These examples showcase the versatility of Vocalizr across different domains and use cases. Each example can be customized and extended based on specific requirements. The key is to leverage Vocalizr's simple API while building robust applications around it.

## Next Steps

- Explore the [API Documentation](API.md) for detailed function references
- Check the [Development Guide](DEVELOPMENT.md) for creating your own integrations
- Review [Configuration](CONFIGURATION.md) for optimizing performance
- See [Troubleshooting](TROUBLESHOOTING.md) for common issues and solutions