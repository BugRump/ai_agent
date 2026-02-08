import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("API Key not found")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent!")
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    if response.usage_metadata == None:
        raise RuntimeError("Failed API request.")
    x = response.usage_metadata.prompt_token_count
    y = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens: {x}")
    print(f"Response tokens: {y}")
    print(f"Response:\n {response.text}")

if __name__ == "__main__":
    main()
