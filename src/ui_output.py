# src/ui_output.py
import pygame
import threading
import os
import time
from rich.console import Console
from rich.live import Live
from rich.text import Text

class SyncOutput:
    def __init__(self):
        self.console = Console()
        # Pygame mixer initialize 
        pygame.mixer.init()

    def _play_audio(self, file_path):
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            # Jab tak audio chal raha hai, wait karein
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
        except Exception as e:
            print(f"Audio Playback Error: {e}")
        finally:
            # File ko delete kar dein taaki disk clean rahe
            if os.path.exists(file_path):
                os.remove(file_path)

    def _type_animation(self, text):
        with Live(Text(""), refresh_per_second=20, console=self.console) as live:
            current_text = ""
            for char in text:
                current_text += char
                live.update(Text(f"🤖: {current_text}", style="bold green"))
                time.sleep(0.02)

    def output(self, text, file_path):
        # Parallel: Play Audio + Text Response
        t1 = threading.Thread(target=self._play_audio, args=(file_path,))
        t2 = threading.Thread(target=self._type_animation, args=(text,))
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()