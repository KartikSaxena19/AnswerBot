# src/llm_hub.py
import requests
from groq import Groq
import config

class LMStudioHub:
    def __init__(self):
        self.provider = config.LLM_PROVIDER
        self.context_buffer = [{"role": "system", "content": config.SYSTEM_PROMPT}]
        
        if self.provider == "groq":
            if not config.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is missing in .env file!")
            self.groq_client = Groq(api_key=config.GROQ_API_KEY)
            self.model_name = "openai/gpt-oss-20b" 
            print("LLM Hub: Using Groq Cloud API")
        else:
            self.base_url = config.LM_STUDIO_URL
            print("LLM Hub: Using Local LM Studio")

    def get_response(self, text):
        self.context_buffer.append({"role": "user", "content": text})
        
        try:
            if self.provider == "groq":
                completion = self.groq_client.chat.completions.create(
                    model=self.model_name,
                    messages=self.context_buffer,
                    temperature=0.7,
                    max_tokens=150,
                )
                reply = completion.choices[0].message.content
            else:
                payload = {
                    "messages": self.context_buffer,
                    "temperature": 0.7,
                    "max_tokens": 150
                }
                response = requests.post(f"{self.base_url}/chat/completions", json=payload)
                reply = response.json()['choices'][0]['message']['content']

            self.context_buffer.append({"role": "assistant", "content": reply})
            
            if len(self.context_buffer) > 6:
                self.context_buffer = [self.context_buffer[0]] + self.context_buffer[-4:]
                
            return reply
            
        except Exception as e:
            print(f"LLM Error: {e}")
            return "I am having trouble connecting to my brain."