# Blazor Web App
The project **Blazor_QnA_OpenAI** is a Blazor WASM app that asks the user for a prompt (in text or voice), uses the Azure Speech SDK to convert voice to text, sends the prompt to the Azure Function API, and displays the response.

## Summary

### Create project
```
dotnet new blazorwasm -o BlazorWAQnAOpenAI --no-https -f net6.0
```

### Add Packages
```
dotnet add package Newtonsoft.Json
dotnet add package Microsoft.CognitiveServices.Speech
```

### Get the prompt from de user and send it to the Azure Functions API

The code to get the prompt from de user and send it to the Azure Functions API is in the file: **Components/CQnAOpenAI.razor**

```
@code {
    private static string InfoPatient = "Historial del paciente:\nNombre completo: JUAN PEREZ PEREZ\nCédula: 1234512345\nNo tiene alergias a ningún medicamento\nNo tiene ninguna cirugía previa\nNo bebe alcohol\nNo fuma\nNo consume drogas\nNo tiene diabetes\nToma Escitalopram para la depresión\nNació el 17 de octubre de 1984\nHombre\nmide 1.75 metros\npesa 61 kilos\nTuvo un sagrado digestivo por úlceras en julio del 2022\nEstuvo hospitalizado por 6 días como consecuencia del sangrado en julio del 2022\nTuvo anemia aguda como consecuencia del sagrado digestivo de julio 2022\nTuvo un segundo sangrado digestivo en Octubre 2022\nEstuvo hospitalizado 2 días en cuidados intensivos por el segundo sangrado digestivo\nRecibió 8 pintas de sangre\nTuvo covid-19 en diciembre de 2022 \nEstuvo hospitalizado 4 días por consecuencia del Covid-19\n";
    private static string QnAResponse = "Respuesta del QnA: ";
    private static string StrPrompt = "Tuvo Covid?";

    private static async Task<string> CallQnAApi()
    {
        Console.WriteLine("Inicio CallQnAApi " + StrPrompt);
        var qnaApiUril = "http://localhost:7071/api/CallQnAApi";
        var qnaApiClient = new HttpClient();
        
        var qnaApiRequest = new HttpRequestMessage(HttpMethod.Post, qnaApiUril);
        qnaApiRequest.Content = new StringContent(JsonConvert.SerializeObject(new { KnowledgeBaseText = InfoPatient, Prompt = StrPrompt }), Encoding.UTF8, "application/json");
        var qnaApiResponse = await qnaApiClient.SendAsync(qnaApiRequest);
        var qnaApiResult = await qnaApiResponse.Content.ReadAsStringAsync();
        QnAResponse = qnaApiResult;
        
        return qnaApiResult;
    }
```

### Speech to Text using Azure Speech SDK

The code to convert the prompt from voice to text uses the Azure Speech JavaScript SDK, since communication with the local computer's microphone cannot be done with Blazor (WebAssembly or server). The code is in **Components/CQnAOpenAI.razor.js**

```
export async function SpeechToTextFromMic() {
    var subscriptionKey = "{Azure Speech Suscription Key}", serviceRegion = "{Azure Speech Region}";
    var SpeechSDK;
    var playbutton;
    var resultText;
    var phraseDiv;
    var resultadoDiv;
    var recognizer;

    playbutton = document.getElementById("playbutton");
    phraseDiv = document.getElementById("txtPrompt");
    resultadoDiv = document.getElementById("txtRespuestaPaciente");    

    if (!!window.SpeechSDK) {
        SpeechSDK = window.SpeechSDK;
        playbutton.disabled = false;

    }

    window.console.log('CLIC!!!');
    var speechConfig = SpeechSDK.SpeechConfig.fromSubscription(subscriptionKey, serviceRegion);

    speechConfig.speechRecognitionLanguage = "es-MX";
    
    var audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();

    recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig);
    phraseDiv.value = "Escuchando...";
    playbutton.disabled = true;
    
    recognizer.recognizeOnceAsync(
        function (result) {
            playbutton.disabled = false;
            if (result.reason === SpeechSDK.ResultReason.RecognizedSpeech) {
                let translation = result.text;
                window.console.log(translation);
                phraseDiv.value = translation;
                resultText = translation;
            }
            DotNet.invokeMethodAsync('BlazorWAQnAOpenAI', 'ReturnPromptAsync', resultText)
                .then(data => {
                    console.log(data);
                    resultadoDiv.value = data;
                });
            recognizer.close();
            recognizer = undefined;
        },
        function (err) {
            playbutton.disabled = false;
            phraseDiv.value = err;
            window.console.log(err);

            recognizer.close();
            recognizer = undefined;
        });

    return resultText;
}
```

## Run the project
Open the project Blazor_QnA_OpenAI in VS Code, edit the file CQnAOpenAI.razor.js and change the next line with your [Azure Speech suscription key](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices) and region
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

## Resource Links:
- [AzureSpeechAndTextAnalytics](https://github.com/DFMERA/AzureSpeechAndTextAnalytics)
- [Call JavaScript functions from .NET methods in ASP.NET Core Blazor](https://learn.microsoft.com/en-us/aspnet/core/blazor/javascript-interoperability/call-javascript-from-dotnet?view=aspnetcore-7.0)
- [Cognitive Services Speech SDK for JavaScript](https://learn.microsoft.com/en-us/javascript/api/overview/azure/microsoft-cognitiveservices-speech-sdk-readme?view=azure-node-latest)
- [Quickstart: Recognize and convert speech to text](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=macos%2Cterminal&pivots=programming-language-javascript)
