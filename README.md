# Enhancing Patient Care with OpenAI: A Blazor and Azure Speech AI Medical Assistant Web App

This project is a sample application that uses [OpenAI](https://openai.com) and Azure Speech to create a QnA "Medical Assistant". It can answer questions about a patient's medical history in natural language, much like [ChatGPT](https://chat.openai.com) but with its own knowledge base.

![OpenAI Medical Assistant](https://github.com/DFMERA/OpenAI_Medical_Assistant/blob/main/img/OpenAI_Medical_Assistant.gif)

## Components
The project has two principal components.

### OpenAI QnA API
The project **Azure_Functions_OpenAI** is an Azure Function API that uses the OpenAI Python SDK to send the request to OpenAI service and returns the response

### Blazor Web App
The project **Blazor_QnA_OpenAI** is a Blazor WASM app that asks the user for a prompt (in text or voice), uses the Azure Speech SDK to convert voice to text, sends the prompt to the Azure Function API, and displays the response.

## Prerequisites
- [Visual Studio Code](https://code.visualstudio.com)
- [Azure Functions SDK](https://azure.microsoft.com/en-us/downloads/)
- [.NET 6.0 (or later)](https://dotnet.microsoft.com/en-us/download)
- [OpenAI suscription key](https://platform.openai.com/docs/introduction)
- [Azure Speech suscription key](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/index-speech-to-text)

## Run the Project
First, we need to run the Azure Functions API, open the project Azure_Functions_OpenAI in VS Code, edit the file local.settings.json and change the next key with your [OpenAI suscription key](https://platform.openai.com/docs/introduction)
```
"OPENAI_API_KEY": "{OpenAI KEY}"
```
Then open a terminal to run the command:
```
func start
```
The API runs in ```http://localhost:7071/api/CallQnAApi```

Second, we need to run the web project, open the project Blazor_QnA_OpenAI in VS Code, edit the file CQnAOpenAI.razor.js and change the next line with your [Azure Speech suscription key](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices) and region
```
var subscriptionKey = "{Azure Speech Suscription Key}", serviceRegion = "{Azure Speech Region}";
```
If you want the project to understand you in English you have to change the value of the next line to **en-US**
```
speechConfig.speechRecognitionLanguage = "es-MX";
```
Then open a terminal to run the command:
```
dotnet watch
```
The project runs in ```http://localhost:5082```

You can change the dummy patient history and ask any question about the history in text or by voice. Much like [ChatGPT](https://chat.openai.com) it will understand the natural language and give you a response.
