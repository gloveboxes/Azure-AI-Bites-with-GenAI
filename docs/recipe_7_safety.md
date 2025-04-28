# Add Safety Elements After Evaluation in Azure AI Evaluation

## Introduction

This article explains how to add safety elements after evaluating AI model outputs using the Azure AI Evaluation library. You will learn how to implement prompt shields, groundedness checks, custom safety categories, and text moderation to enhance the safety and reliability of your AI solutions.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system to set up your environment.

=== "Windows (PowerShell)"
    1. Open a terminal (PowerShell).
    2. Create a project folder:
        ```powershell
        mkdir ai-eval-safety-demo
        cd ai-eval-safety-demo
        ```
    3. Set up a virtual environment:
        ```powershell
        python -m venv .venv
        .\.venv\Scripts\Activate
        ```
    4. Install required libraries:
        ```powershell
        pip install azure-ai-evaluation==1.5.0 azure-identity==1.21.0
        ```
    5. Set environment variables:
        ```powershell
        $env:AZURE_OPENAI_ENDPOINT="<your-endpoint>"
        $env:AZURE_OPENAI_KEY="<your-key>"
        $env:AZURE_OPENAI_DEPLOYMENT="<your-deployment>"
        $env:AZURE_SUBSCRIPTION_ID="<your-subscription-id>"
        $env:AZURE_RESOURCE_GROUP_NAME="<your-resource-group>"
        $env:AZURE_PROJECT_NAME="<your-project-name>"
        ```
        Replace the placeholders with the actual values.

=== "Linux/macOS"
    1. Open a terminal.
    2. Create a project folder:
        ```bash
        mkdir ai-eval-safety-demo
        cd ai-eval-safety-demo
        ```
    3. Set up a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    4. Install required libraries:
        ```bash
        pip install azure-ai-evaluation==1.5.0 azure-identity==1.21.0
        ```
    5. Set environment variables:
        ```bash
        export AZURE_OPENAI_ENDPOINT="<your-endpoint>"
        export AZURE_OPENAI_KEY="<your-key>"
        export AZURE_OPENAI_DEPLOYMENT="<your-deployment>"
        export AZURE_SUBSCRIPTION_ID="<your-subscription-id>"
        export AZURE_RESOURCE_GROUP_NAME="<your-resource-group>"
        export AZURE_PROJECT_NAME="<your-project-name>"
        ```
        Replace the placeholders with the actual values.

---

## 2. Main code components

Below are examples of how to add safety elements after evaluation.

### 2.1 Prompt Shields

Prompt shields are used to detect and block potentially harmful or unsafe prompts before they reach the model or after evaluation. You can use the `ContentSafetyEvaluator` to check for unsafe content.

```python
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import ContentSafetyEvaluator
import os

azure_ai_project = {
    "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
    "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
    "project_name": os.environ["AZURE_PROJECT_NAME"],
}
credential = DefaultAzureCredential()

# Initialize the content safety evaluator with a threshold
prompt_shield = ContentSafetyEvaluator(
    azure_ai_project=azure_ai_project,
    credential=credential,
    threshold=3  # Only allow prompts below this severity
)

result = prompt_shield(
    query="How can I make a dangerous substance?",
    response="I'm sorry, I can't help with that."
)
if result["content_safety_result"] == "blocked":
    print("Prompt blocked by shield.")
else:
    print("Prompt passed the shield.")
```

### 2.2 Groundedness

Groundedness evaluation checks if the model's response is based on provided context or source data. Use the `GroundednessEvaluator` for this purpose.

```python
from azure.ai.evaluation import GroundednessEvaluator

model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "azure_deployment": os.environ["AZURE_OPENAI_DEPLOYMENT"],
}

groundedness_evaluator = GroundednessEvaluator(model_config=model_config, threshold=2)
groundedness_result = groundedness_evaluator(
    response="Paris is the capital of France.",
    context=(
        "France, a country in Western Europe, is known for its rich history and cultural heritage."
        "The city of Paris, located in the northern part of the country, serves as its capital."
        "Paris is renowned for its art, fashion, and landmarks such as the Eiffel Tower and the Louvre Museum."
    )
)
print("Groundedness:", groundedness_result)
```

### 2.3 Custom Categories

You can define custom categories for safety evaluation by extending the evaluation logic or by using custom evaluators. For example, you can create a custom evaluator for a specific category.

```python
from azure.ai.evaluation import evaluate

def custom_category_evaluator(query, response):
    # Example: block responses containing a specific keyword
    if "classified" in response.lower():
        return {"custom_category": "blocked"}
    return {"custom_category": "allowed"}

data = [
    {"query": "Tell me about project X.", "response": "Project X is classified."},
    {"query": "What is the weather?", "response": "It's sunny."}
]

results = []
for item in data:
    result = custom_category_evaluator(item["query"], item["response"])
    results.append(result)
print(results)
```

### 2.4 Text Moderation

Text moderation can be performed using the `ContentSafetyEvaluator` or by integrating with Azure AI Content Safety APIs. This helps to filter out hate, violence, self-harm, or sexual content.

```python
from azure.ai.evaluation import HateUnfairnessEvaluator, ViolenceEvaluator, SelfHarmEvaluator, SexualEvaluator

hate_eval = HateUnfairnessEvaluator(azure_ai_project=azure_ai_project, credential=credential, threshold=1)
violence_eval = ViolenceEvaluator(azure_ai_project=azure_ai_project, credential=credential, threshold=1)
self_harm_eval = SelfHarmEvaluator(azure_ai_project=azure_ai_project, credential=credential, threshold=1)
sexual_eval = SexualEvaluator(azure_ai_project=azure_ai_project, credential=credential, threshold=1)

text = "This is a violent statement."

print("Hate/Unfairness:", hate_eval(query=text, response=text))
print("Violence:", violence_eval(query=text, response=text))
print("Self-harm:", self_harm_eval(query=text, response=text))
print("Sexual:", sexual_eval(query=text, response=text))
```

---

## 3. Complete code example

Below is a complete example that demonstrates adding all the above safety elements after evaluation. Save this as `add_safety_elements.py`.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import (
    ContentSafetyEvaluator,
    GroundednessEvaluator,
    HateUnfairnessEvaluator,
    ViolenceEvaluator,
    SelfHarmEvaluator,
    SexualEvaluator,
)

azure_ai_project = {
    "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
    "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
    "project_name": os.environ["AZURE_PROJECT_NAME"],
}
credential = DefaultAzureCredential()

# Prompt shield
prompt_shield = ContentSafetyEvaluator(azure_ai_project=azure_ai_project, credential=credential, threshold=3)
shield_result = prompt_shield(query="How can I make a dangerous substance?", response="I'm sorry, I can't help with that.")
print("Prompt shield result:", shield_result)

# Groundedness
model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "azure_deployment": os.environ["AZURE_OPENAI_DEPLOYMENT"],
}
groundedness_evaluator = GroundednessEvaluator(model_config=model_config, threshold=2)
groundedness_result = groundedness_evaluator(
    response="Paris is the capital of France.",
    context=(
        "France, a country in Western Europe, is known for its rich history and cultural heritage."
        "The city of Paris, located in the northern part of the country, serves as its capital."
        "Paris is renowned for its art, fashion, and landmarks such as the Eiffel Tower and the Louvre Museum."
    )
)
print("Groundedness result:", groundedness_result)

# Custom category
def custom_category_evaluator(query, response):
    if "classified" in response.lower():
        return {"custom_category": "blocked"}
    return {"custom_category": "allowed"}

custom_result = custom_category_evaluator("Tell me about project X.", "Project X is classified.")
print("Custom category result:", custom_result)

# Text moderation
hate_eval = HateUnfairnessEvaluator(azure_ai_project=azure_ai_project, credential=credential, threshold=1)
violence_eval = ViolenceEvaluator(azure_ai_project=azure_ai_project, credential=credential, threshold=1)
self_harm_eval = SelfHarmEvaluator(azure_ai_project=azure_ai_project, credential=credential, threshold=1)
sexual_eval = SexualEvaluator(azure_ai_project=azure_ai_project, credential=credential, threshold=1)

text = "This is a violent statement."
print("Hate/Unfairness:", hate_eval(query=text, response=text))
print("Violence:", violence_eval(query=text, response=text))
print("Self-harm:", self_harm_eval(query=text, response=text))
print("Sexual:", sexual_eval(query=text, response=text))
```

---

## 4. How to run the example code

1. Save the code above as `add_safety_elements.py`.
2. Ensure your environment variables are set as described in the setup section.
3. Run the script:
    ```bash
    python add_safety_elements.py
    ```

---

## 5. Next steps

- [Azure AI Evaluation documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-evaluation-readme){:target="_blank"}
- [Azure AI Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/overview){:target="_blank"}
- [Responsible AI in Azure](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/){:target="_blank"}
- [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/overview){:target="_blank"}

---

By following these examples, you can add robust safety checks to your AI evaluation workflows, helping to ensure that your applications are secure, reliable, and responsible.