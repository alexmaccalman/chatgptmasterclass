import logging
import openai
from dotenv import load_dotenv, find_dotenv
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.functions as func

# sample request body
# {"model": "davinci", "prompt": "give me a slogan for a cookie company", "max_tokens": 200, "temperature": 0}


_ = load_dotenv(find_dotenv())  # read local .env file

# Azure Key Vault configuration
vault_url = "https://resumekeyvaultadm.vault.azure.net/"
secret_name = "OPENAI-API-KEY"

# Create a DefaultAzureCredential object to authenticate with Azure Key Vault
credential = DefaultAzureCredential()

# Create a SecretClient to access the Azure Key Vault
secret_client = SecretClient(vault_url=vault_url, credential=credential)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve the OPENAI_API_KEY from Azure Key Vault
    secret_key = secret_client.get_secret(secret_name).value

    # Give OpenAI our secret_key to authenticate
    openai.api_key = secret_key

    # Rest of your code...
    req_body = req.get_json()

    # Call the OpenAI API
    output = openai.Completion.create(
        model=req_body['model'],
        prompt=req_body['prompt'],
        max_tokens=req_body['max_tokens'],
        temperature=req_body['temperature'],
    )

    # Format the response
    output_text = output['choices'][0]['text']

    # Echo the response
    return func.HttpResponse(output_text, status_code=200)
