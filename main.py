# main.py
import sys
import string
from src.audio_input import AudioInput
from src.transcriber import Transcriber
from src.llm_hub import LMStudioHub
from src.tts_engine import MiraTTS
from src.ui_output import SyncOutput
from src.shadow_listener import ShadowListener
import config

def check_commands(transcription, command_list):
    """Transcription ko clean karke check karta hai ki command match hui ya nahi."""
    if not transcription:
        return False
    # Punctuation (.,!?) hata dein aur lowercase karein
    text = transcription.lower().translate(str.maketrans('', '', string.punctuation))
    return any(cmd in text for cmd in command_list)

def main():
    print("=== INIT: Loading Models ===")
    audio_in = AudioInput()
    transcriber = Transcriber()
    llm = LMStudioHub()
    tts = MiraTTS()
    output = SyncOutput()
    
    while True: 
        print("\n=== SHADOW LISTENER: Waiting for Activation ===")
        
        # Transcriber pass karein taaki baar-baar load na ho
        shadow = ShadowListener(audio_in, transcriber)
        shadow.run() 
        
        print("ACTIVE: Session Started!")
        
        state = "MIC_STREAMING"
        audio_buffer = []
        silence_counter = 0
        
        # Inner loop for active conversation
        while state == "MIC_STREAMING":
            data, is_speech = audio_in.read_chunk()
            audio_buffer.append(data)
            
            if is_speech:
                silence_counter = 0
            else:
                silence_counter += 1
                
            # Silence detected
            if silence_counter > config.SILENCE_THRESHOLD_CHUNKS:
                state = "PROCESSING"
                print("Silence detected. Processing...")
                
                transcription = transcriber.transcribe(audio_buffer)
                print(f"👤 You: {transcription}")
                
                # Khaali transcription ignore karein
                if not transcription or transcription.strip() == "":
                    print("No voice detected, Speak Again...")
                    audio_buffer = []
                    silence_counter = 0
                    state = "MIC_STREAMING"
                    continue
                
                # COMMAND LOGIC (Pause / Terminate)
                if check_commands(transcription, config.TERMINATE_COMMANDS):
                    print("🛑 TERMINATE command detected. Shutting down...")
                    audio_in.cleanup()
                    sys.exit(0)
                    
                elif check_commands(transcription, config.PAUSE_COMMANDS):
                    print("⏸️ PAUSE command detected. Returning to Shadow Listener.")
                    break # Breaks inner loop, goes back to Shadow Listener (Outer loop)
                
                # NORMAL LLM RESPONSE 
                llm_response = llm.get_response(transcription)
                
                # Generate Audio File
                audio_file = tts.generate_audio(llm_response) 
                
                # Parallel: Play Audio + Text Response
                output.output(llm_response, audio_file)      
                
                # Reset for next interaction
                audio_buffer = []
                silence_counter = 0
                state = "MIC_STREAMING"
                print("\nListening... (Say 'Pause' to sleep, 'Terminate' to quit)")

if __name__ == "__main__":
    main()