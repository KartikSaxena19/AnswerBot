import pyaudio
import webrtcvad
import config

class AudioInput:
    def __init__(self):
        self.rate = 16000
        self.chunk_size = int(self.rate * 30 / 1000) 
        self.vad = webrtcvad.Vad(config.VAD_AGGRESSIVENESS)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

    def read_chunk(self):
        data = self.stream.read(self.chunk_size, exception_on_overflow=False)
        is_speech = self.vad.is_speech(data, self.rate)
        return data, is_speech

    def cleanup(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()