# 1. What you'll learn
- How to create a Python virtual environment  
- How to install the minimum required Azure SDK packages  
- How to set up the required environment variables  
- How to break down a “chat completions with history” sample into logical components  
- How to run the sample end‑to‑end  

# 2. Prerequisites & creating a virtual environment
1. **Python 3.8+** installed on your machine  
2. Open your terminal and navigate to your project folder  
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # macOS/Linux
   .\.venv\Scripts\activate     # Windows
   ```

# 3. Install dependencies
Only the libraries used by this sample are installed:
```bash
pip install   azure-ai-inference==1.0.0b9   azure-core==1.33.0
```

# 4. Set environment variables
The sample expects two variables. On macOS/Linux add these to `~/.bashrc` or `~/.zshrc`, or set in your CI/CD pipeline:
```bash
export AZURE_AI_CHAT_ENDPOINT="https://<your-deployment-name>.<your-azure-region>.models.ai.azure.com"
export AZURE_AI_CHAT_KEY="<your-model-key>"
```
On Windows (PowerShell):
```powershell
setx AZURE_AI_CHAT_ENDPOINT "https://<your-deployment-name>.<your-azure-region>.models.ai.azure.com"
setx AZURE_AI_CHAT_KEY "<your-model-key>"
```

# 5. Code breakdown
Below is a step‑by‑step explanation of the sample:

### 5.1 Load environment variables  
```python
import os

try:
    endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
    key      = os.environ["AZURE_AI_CHAT_KEY"]
except KeyError:
    print("Missing AZURE_AI_CHAT_ENDPOINT or AZURE_AI_CHAT_KEY")
    exit(1)
```
- Reads your endpoint and key, and exits if they’re not set.

### 5.2 Import Azure SDK clients & message types  
```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
```
- `ChatCompletionsClient` handles calls to the chat endpoint.  
- `SystemMessage`, `UserMessage`, `AssistantMessage` model the conversation.  
- `AzureKeyCredential` wraps your key for authentication.

### 5.3 Create the client and send two chat requests  
```python
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# 1st turn
messages = [
    SystemMessage("You are an AI assistant that helps people find information. Replies must be ≤2 sentences."),
    UserMessage("What year was construction of the international space station mostly done?")
]
response = client.complete(messages=messages)
print(response.choices[0].message.content)

# 2nd turn (history included)
messages.append(AssistantMessage(response.choices[0].message.content))
messages.append(UserMessage("And what was the estimated cost to build it?"))
response = client.complete(messages=messages)
print(response.choices[0].message.content)
```
- Initializes the chat client  
- Sends one question, prints the answer  
- Appends the assistant’s reply and a follow‑up question to the `messages` list  
- Sends the second request with full history  

# 6. Complete code
```python
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def sample_chat_completions_with_history():
    try:
        endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
        key      = os.environ["AZURE_AI_CHAT_KEY"]
    except KeyError:
        print("Missing AZURE_AI_CHAT_ENDPOINT or AZURE_AI_CHAT_KEY")
        exit(1)

    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # First turn
    messages = [
        SystemMessage("You are an AI assistant that helps people find information. Replies must be ≤2 sentences."),
        UserMessage("What year was construction of the international space station mostly done?")
    ]
    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

    # Second turn (history included)
    messages.append(AssistantMessage(response.choices[0].message.content))
    messages.append(UserMessage("And what was the estimated cost to build it?"))
    response = client.complete(messages=messages)
    print(response.choices[0].message.content)


if __name__ == "__main__":
    sample_chat_completions_with_history()
```

# 7. How to run the code
1. Ensure your virtual environment is active.  
2. Verify the environment variables are set:  
   ```bash
   echo $AZURE_AI_CHAT_ENDPOINT
   echo $AZURE_AI_CHAT_KEY
   ```  
3. Run the sample:
   ```bash
   python sample_chat_completions_with_history.py
   ```

# 8. Resources
1. **Azure AI Inference SDK docs**  
   https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference  
2. **AzureKeyCredential reference**  
   https://learn.microsoft.com/python/api/azure-core/azure.core.credentials.azurekeycredential  
3. **GitHub Models chat completions guide**  
   https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/README.md#chat-completions  
