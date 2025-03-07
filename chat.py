from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from a .env file
load_dotenv()

# Initialize OpenAI client with the API key from environment variables
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def chat_completion(prompt, agent):
    '''Generate a chat completion based on a given prompt and agent model'''
    completion = client.chat.completions.create(
        model=agent,
        max_tokens=100,
        messages=[
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content  # Get the response from the completion
    return response

def evaluate_problem(prompt, agent):
    '''Evaluate a problem and return a rating from 1 (easy) to 10 (very difficult)'''
    completion = client.chat.completions.create(
        model=agent,
        max_tokens=300,
        messages=[
            {"role": "system", "content": "Rate this problem from 1 (easy) to 10 (very difficult). Just return a number."},
            {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content  # Get the rating from the completion
    return response

if __name__ == "__main__":
    chat_completion()  # Run the chat completion function
