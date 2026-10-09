# src/tts_engine.py
import edge_tts
import asyncio
import os

class MiraTTS:
    def __init__(self):
        self.voice = "en-US-ChristopherNeural"
        self.temp_file = "temp_response.mp3"

    def generate_audio(self, text):
        async def _generate():
            communicate = edge_tts.Communicate(text, self.voice)
            # MP3 file mein save karein
            await communicate.save(self.temp_file)
            
        asyncio.run(_generate())
        return self.temp_file