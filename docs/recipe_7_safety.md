# Add Safety Elements After Evaluation in Azure AI Evaluation

## Introduction

After evaluating AI model outputs, you may need to add safety elements to ensure responsible and secure use of generative AI. This guide explains how to add safety elements such as prompt shields, groundedness checks, custom safety categories, and text moderation using the Azure AI Evaluation library. The goal is to help you integrate these safety checks into your evaluation workflow.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system tab and follow the steps to set up your environment.

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a project folder:
        ```powershell
        mkdir ai-eval-safety
        cd ai-eval-safety
        ```
    3. Set up a virtual environment:
        ```powershell
        python -m venv .venv
        ```
    4. Activate the virtual environment:
        ```powershell
        .\.venv\Scripts\Activate
        ```
    5. Install the required libraries:
        ```powershell
        pip install azure-ai-evaluation==1.5.0 azure-identity==1.21.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:AZURE_SUBSCRIPTION_ID="<your-subscription-id>"
        $env:AZURE_RESOURCE_GROUP_NAME="<your-resource-group>"
        $env:AZURE_PROJECT_NAME="<your-project-name>"
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a project folder:
        ```bash
        mkdir ai-eval-safety
        cd ai-eval-safety
        ```
    3. Set up a virtual environment:
        ```bash
        python3 -m venv .venv
        ```
    4. Activate the virtual environment:
        ```bash
        source .venv/bin/activate
        ```
    5. Install the required libraries:
        ```bash
        pip install azure-ai-evaluation==1.5.0 azure-identity==1.21.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```bash
        export AZURE_SUBSCRIPTION_ID="<your-subscription-id>"
        export AZURE_RESOURCE_GROUP_NAME="<your-resource-group>"
        export AZURE_PROJECT_NAME="<your-project-name>"
        ```

## 2. Main code components

### 2.1 Prompt Shields

Prompt shields help detect and block potentially harmful or adversarial prompts before they reach the model. You can use the `ContentSafetyEvaluator` to screen prompts.

**Example:**

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

prompt_shield = ContentSafetyEvaluator(azure_ai_project=azure_ai_project, credential=credential)
result = prompt_shield(query="Write a dangerous script", response="Here is a script...")
print(result)
```

### 2.2 Groundedness

Groundedness checks ensure that model responses are based on provided context or source data, reducing hallucinations.

**Example:**

```python
from azure.ai.evaluation import GroundednessEvaluator

model_config = {
    "azure_endpoint": "<your-aoai-endpoint>",
    "api_key": "<your-aoai-key>",
    "azure_deployment": "<your-aoai-deployment>",
}

groundedness_eval = GroundednessEvaluator(model_config=model_config)
result = groundedness_eval(
    response="The capital of France is Paris.",
    context="France's capital is Paris."
)
print(result)
```

### 2.3 Custom Categories

You can define and evaluate custom safety categories by extending or configuring evaluators.

**Example:**

```python
from azure.ai.evaluation import HateUnfairnessEvaluator

hate_unfairness_eval = HateUnfairnessEvaluator(azure_ai_project=azure_ai_project, credential=credential)
result = hate_unfairness_eval(
    query="Tell me a joke about a nationality.",
    response="..."
)
print(result)
```

You can create your own evaluator by subclassing or configuring existing ones for your custom category.

### 2.4 Text Moderation

Text moderation screens responses for content such as violence, self-harm, or sexual content.

**Example:**

```python
from azure.ai.evaluation import ViolenceEvaluator, SelfHarmEvaluator, SexualEvaluator

violence_eval = ViolenceEvaluator(azure_ai_project=azure_ai_project, credential=credential)
self_harm_eval = SelfHarmEvaluator(azure_ai_project=azure_ai_project, credential=credential)
sexual_eval = SexualEvaluator(azure_ai_project=azure_ai_project, credential=credential)

violence_result = violence_eval(query="...", response="...")
self_harm_result = self_harm_eval(query="...", response="...")
sexual_result = sexual_eval(query="...", response="...")

print(violence_result)
print(self_harm_result)
print(sexual_result)
```

## 3. Complete code example

The following example demonstrates how to add multiple safety elements after evaluation. Save this as `add_safety_after_evaluation.py`.

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

# Set up Azure AI project and credentials
azure_ai_project = {
    "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
    "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
    "project_name": os.environ["AZURE_PROJECT_NAME"],
}
credential = DefaultAzureCredential()

# Example prompt and response
prompt = "Write a dangerous script"
response = "Here is a script that could be harmful..."

# 1. Prompt shield
prompt_shield = ContentSafetyEvaluator(azure_ai_project=azure_ai_project, credential=credential)
shield_result = prompt_shield(query=prompt, response=response)
print("Prompt Shield Result:", shield_result)

# 2. Groundedness
model_config = {
    "azure_endpoint": "<your-aoai-endpoint>",
    "api_key": "<your-aoai-key>",
    "azure_deployment": "<your-aoai-deployment>",
}
groundedness_eval = GroundednessEvaluator(model_config=model_config)
groundedness_result = groundedness_eval(
    response="The capital of France is Paris.",
    context="France's capital is Paris."
)
print("Groundedness Result:", groundedness_result)

# 3. Custom category (hate/unfairness)
hate_unfairness_eval = HateUnfairnessEvaluator(azure_ai_project=azure_ai_project, credential=credential)
hate_result = hate_unfairness_eval(query=prompt, response=response)
print("Hate/Unfairness Result:", hate_result)

# 4. Text moderation (violence, self-harm, sexual)
violence_eval = ViolenceEvaluator(azure_ai_project=azure_ai_project, credential=credential)
self_harm_eval = SelfHarmEvaluator(azure_ai_project=azure_ai_project, credential=credential)
sexual_eval = SexualEvaluator(azure_ai_project=azure_ai_project, credential=credential)

violence_result = violence_eval(query=prompt, response=response)
self_harm_result = self_harm_eval(query=prompt, response=response)
sexual_result = sexual_eval(query=prompt, response=response)

print("Violence Result:", violence_result)
print("Self-Harm Result:", self_harm_result)
print("Sexual Content Result:", sexual_result)
```

## 4. How to run the example code

1. Save the code above as `add_safety_after_evaluation.py`.
2. Ensure your environment variables are set and your virtual environment is activated.
3. Run the script:

    ```bash
    python add_safety_after_evaluation.py
    ```

## 5. Next steps

- [Azure AI Evaluation documentation](https://learn.microsoft.com/azure/ai-services/evaluation/){:target="_blank"}
- [Responsible AI in Azure](https://learn.microsoft.com/azure/ai-services/responsible-ai/){:target="_blank"}
- [Azure AI Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/overview){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}

By integrating these safety elements, you can help ensure your AI applications are secure, responsible, and compliant with organizational and regulatory requirements.