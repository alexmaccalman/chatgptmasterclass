import openai
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(prompt, model="text-davinci-003", temperature=0.0):
    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=200,
            temperature=temperature,
        )
        # return response.choices[0].text
        return response
    except openai.OpenAIError as e:
        error_message = str(e)
        return f"Error: {error_message}"
    
prompt = 'Tell me a slogan for a home security company'
output = get_completion(prompt)['choices'][0]['text']
print(output)