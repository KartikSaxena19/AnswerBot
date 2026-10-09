import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")

WHISPER_MODEL_SIZE = "base" # "tiny" or "base" 
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8" 

SYSTEM_PROMPT = "You are a helpful, concise voice assistant. Keep answers under 3 sentences."

VAD_AGGRESSIVENESS = 1 
SILENCE_THRESHOLD_CHUNKS = 50

ACTIVATE_COMMANDS = ["start", "hey", "continue"]
PAUSE_COMMANDS = ["pause", "exit", "quit", "goodbye"]
TERMINATE_COMMANDS = ["deactivate", "terminate", "shut down"]