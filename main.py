import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("API Key not found")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent!")
    
    parser = argparse.ArgumentParser(description="AI_Bot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages
        )
    
    if response.usage_metadata == None:
        raise RuntimeError("Failed API request.")
    
    x = response.usage_metadata.prompt_token_count
    y = response.usage_metadata.candidates_token_count
    
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {x}")
        print(f"Response tokens: {y}")
        
    print(f"Response:\n {response.text}")

if __name__ == "__main__":
    main()
