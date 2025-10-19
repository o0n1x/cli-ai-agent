import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

import argparse





def main():
    load_dotenv()
    #api
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    #arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="prompt the ai agent",type=str)
    parser.add_argument("-v","--verbose", help="increase output verbosity",action="store_true")
    args = parser.parse_args()
    prompt = args.prompt


    #gemini api call
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    response = client.models.generate_content(model ="gemini-2.0-flash-001",contents=messages)


    #output
    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(response.text)







main()