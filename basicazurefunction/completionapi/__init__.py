import logging
import openai
from dotenv import load_dotenv, find_dotenv
import os
import azure.functions as func

_ = load_dotenv(find_dotenv())  # read local .env file
secret_key = os.getenv("OPENAI_API_KEY")

# sample request body
 # {"model":"text-davinci-003", "prompt":"Tell me a slogan for a home security company", "max_tokens": 200, "temperature": 0.0}

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # give OpenAI our secret_key to authenticate
    openai.api_key = secret_key

    # get variables from the HTTP response
    req_body = req.get_json()
    #comment 2
    # call the OpenAI API
    output = openai.Completion.create(
        model=req_body['model'],
        prompt=req_body['prompt'],
        max_tokens=req_body['max_tokens'],
        temperature=req_body['temperature'],
    )
    # format the response
    output_text = output['choices'][0]['text']
    # echo the response


    return func.HttpResponse(output_text, status_code=200)
