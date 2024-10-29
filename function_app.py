import os
import logging
import azure.functions as func
from openai import AzureOpenAI

# Initialize the Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Environment variables for OpenAI setup
endpoint = os.getenv("ENDPOINT_URL", "https://suman-m2ubs9ew-westeurope.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "ac452e3cc24c4ddc9877dad88fe00383")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the 'name' parameter from the query string or request body
    query = req.params.get('query')
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            query = req_body.get('query')

    if query:
        # Prepare the chat prompt with user's input
        chat_prompt = [
            {"role": "system", "content": "You are an AI assistant that helps people find information."},
            {"role": "user", "content": query}  # User input goes here
        ]

    
        # Call the OpenAI API to get a response
        completion = client.chat.completions.create(
            model=deployment,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
        # Extract the content from the response
        response_content = completion.choices[0]
        logging.info(response_content)
        logging.info(type(response_content))
        return func.HttpResponse(response_content.to_json(),status_code=200)


    # Default response if no name is provided
    return func.HttpResponse(
        status_code=400
    )
