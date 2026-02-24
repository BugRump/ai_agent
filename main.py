import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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

    for i in range(20):       
        response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],
                                           system_instruction=system_prompt),
        )
    
        if response.usage_metadata == None:
            raise RuntimeError("Failed API request.")
    
        x = response.usage_metadata.prompt_token_count
        y = response.usage_metadata.candidates_token_count
    
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {x}")
            print(f"Response tokens: {y}")

        try:
            for x in response.candidates:
                messages.append(x.content)
        except Exception as e:
            print(f"Error processing response candidates: {e}")
            continue
        
        function_results = []

        if response.function_calls != None:
            for function_call in response.function_calls:
                function_response = call_function(function_call, verbose=args.verbose)
                if len(function_response.parts) == 0:
                    raise Exception("Function response is empty.")
                elif function_response.parts[0].function_response == None:
                    raise Exception("Function response is None.")
                elif function_response.parts[0].function_response.response == None:
                    raise Exception("Function response content is None.")
                function_results.append(function_response.parts[0])
                
                if args.verbose:
                    print(f"-> {function_response.parts[0].function_response.response}")
        else:
            print(f"Response:\n {response.text}")
            break
        
        messages.append(types.Content(role="user", parts=function_results))

        function_results = []  # Reset function results for next iteration

        # if the end of the range is reached without a break, print the final response and exit with a code of 1 to indicate that the conversation did not reach a natural conclusion within the expected number of iterations
        if i == 19 and response.function_calls != None:
            print(f"Final response:\n {response.text}")
            print("Reached maximum iterations without a natural conclusion.")
            sys.exit(1)

if __name__ == "__main__":
    main()