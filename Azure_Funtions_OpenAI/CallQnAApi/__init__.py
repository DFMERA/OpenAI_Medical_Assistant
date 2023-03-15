import logging
import os
import openai
import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        kbText = req_body.get('KnowledgeBaseText')
        prompt = req_body.get('Prompt')

    if prompt:

        openai.api_key = os.environ["OPENAI_API_KEY"]

        start_sequence = "\nA:"
        restart_sequence = "\n\nQ: "
        prompt_formated = kbText + "\nQ: " + prompt + start_sequence

        response = openai.Completion.create(
         model="text-davinci-003",
         prompt=prompt_formated,
         temperature=0,
         max_tokens=300,
         top_p=1,
         frequency_penalty=0,
         presence_penalty=0,
         stop=["\n"]
        )

        #If the response code is 200, then the request was successful
        if response:
            #get the response as a json object
            response_json = {"Response": response.choices[0].text.strip()}

        return func.HttpResponse(json.dumps(response_json, ensure_ascii=False), status_code=200, mimetype="application/json", charset="utf-8", headers={"Access-Control-Allow-Origin": "*"})
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a prompt in the query string or in the request body for a personalized response.",
             status_code=200
        )
