# src/shadow_listener.py
import threading
import config

class ShadowListener:
    def __init__(self, audio_in, transcriber):
        self.audio_in = audio_in      # Main se pass kiya gaya AudioInput
        self.transcriber = transcriber
        self.wake_word_detected = threading.Event()

    def run(self):
        print(f"Shadow Listener: Waiting for wake word... (Say: {config.ACTIVATE_COMMANDS})")
        audio_buffer = []
        silence_counter = 0
        speech_detected = False
        
        while True:
            data, is_speech = self.audio_in.read_chunk()
            audio_buffer.append(data)
            
            if is_speech:
                silence_counter = 0
                speech_detected = True
            else:
                silence_counter += 1
                
            # 0.5 second ki silence ke baad check
            if silence_counter > 15: 
                if speech_detected:
                    text = self.transcriber.transcribe(audio_buffer).lower()
                    
                    # Buffer reset karein
                    audio_buffer = []
                    silence_counter = 0
                    speech_detected = False
                    
                    # Check karein ki kya user ne wake word bola?
                    if any(cmd in text for cmd in config.ACTIVATE_COMMANDS):
                        self.wake_word_detected.set()
                        break
                else:
                    # Agar sirf background noise thi, toh buffer clear kar dein
                    audio_buffer = []
                    silence_counter = 0