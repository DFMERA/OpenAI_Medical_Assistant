# OpenAI QnA API
The project **Azure_Functions_OpenAI** is an Azure Function API that uses the OpenAI Python SDK to send the request to OpenAI service and returns the response

## Prerequisites
- [Visual Studio Code](https://code.visualstudio.com)
- [Visual Studio Azure Extensions](https://code.visualstudio.com/docs/azure/extensions)
- [Azure Functions SDK](https://azure.microsoft.com/en-us/downloads/)
- [OpenAI suscription key](https://platform.openai.com/docs/introduction)

## Summary

### Create project
Create an [Azure Functions Project](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-configuration) using Visual Studio Code

### Send a request to OpenAI service 
We use the OpenAI Python SDK to send a request to OpenAI service

```
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
```

## Run the Project
First, we need to run the Azure Functions API, open the project Azure_Functions_OpenAI in VS Code, edit the file local.settings.json and change the next key with your [OpenAI suscription key](https://platform.openai.com/docs/introduction)
```
"OPENAI_API_KEY": "{OpenAI KEY}"
```
You can debug the project in VS Code or open a terminal to run the command:
```
func start
```
The API runs in ```http://localhost:7071/api/CallQnAApi```

## Test the API
You can test the API with the examples in the file sample.http using VS Code
```
POST http://localhost:7071/api/CallQnAApi
Content-Type: application/json

{
  "KnowledgeBaseText": "Historial del paciente:\nNo tiene alergias a ningún medicamento\nNo tiene ninguna cirugia previa\nNo bebe alcohol\nNo fuma\nNo consume drogas\nToma medicación para la depresión\nNació el 17 de octubre de 1984\nHombre\nmide 1.75 metros\npesa 61 kilos\nTuvo un sagrado digestivo por ulceras en julio del 2022\nTuvo anemia aguda como consecuencia del sagrado digestivo de julio 2022\nEstuvo hospitalizado 3 veces por el sangrado digestivo\nRecibió 8 pintas de sangre\nTuvo covid en diciembre de 2022\nEstuvo hospitalizado por consecuencia del Covid\n",
  "Prompt": "Tiene cirugías?"
}
```

## Pro Tip:
If you are developing in a Mac M1 or an ARM architecture you need to install Azure Functions SDK and the requirements in x86_64 architecture
```
arch -x86_64 .venv/bin/python -m pip install -r requirements.txt
```
