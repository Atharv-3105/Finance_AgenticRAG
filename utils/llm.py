import os 
from google import genai 
from google.genai import types

async def call_llm(prompt: str, temperature: float = 0.0)-> str:
    
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY2"))
    
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt,
        config=types.GenerateContentConfig(
            temperature = temperature,
            top_p = 1.0,
            top_k = 40,
        )
    )
    
    if not response.text:
        return ""
    
    # parts = response.candidates[0].content.parts
    # text = "".join(part.text for part in parts if hasattr(part, "text"))
    
    return response.text.strip()