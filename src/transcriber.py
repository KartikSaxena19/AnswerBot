from faster_whisper import WhisperModel
import numpy as np
import config

class Transcriber:
    def __init__(self):
        print(f"Loading Whisper model ({config.WHISPER_MODEL_SIZE}) on {config.WHISPER_DEVICE}...")
        self.model = WhisperModel(
            config.WHISPER_MODEL_SIZE, 
            device=config.WHISPER_DEVICE, 
            compute_type=config.WHISPER_COMPUTE_TYPE
        )

    def transcribe(self, audio_chunks):
        if not audio_chunks:
            return ""
        audio_np = np.frombuffer(b"".join(audio_chunks), dtype=np.int16).astype(np.float32) / 32768.0
        segments, _ = self.model.transcribe(audio_np, beam_size=5)
        return " ".join([segment.text for segment in segments]).strip()