# Add Safety Elements After Evaluation in Azure AI Evaluation

## Introduction

After evaluating AI model outputs, you may want to add additional safety elements to ensure responsible and secure AI usage. This document explains how to add safety elements such as prompt shields, groundedness checks, custom categories, and text moderation using the Azure AI Evaluation library. The goal is to help you enhance the safety of your AI solutions by applying these techniques after the initial evaluation phase.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Authentication

Azure AI Foundry provides access to evaluation and safety services. You can authenticate using Azure credentials.

1. Go to the Azure AI Foundry portal.
2. Obtain your Azure subscription, resource group, and project name.
3. Use `DefaultAzureCredential` for authentication in your code.

## 2. Developer environment setup

Select your preferred operating system.

=== "Windows (PowerShell)"

    1. Open a terminal.
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
        .venv\Scripts\Activate
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

## 3. Main code components

Below are examples of how to add safety elements after evaluation.

### 3.1 Prompt Shields

Prompt shields help detect and block potentially harmful or unsafe prompts before they reach the model. You can use the `ContentSafetyEvaluator` to screen prompts.

```python
import os

from azure.ai.evaluation import ContentSafetyEvaluator
from azure.identity import DefaultAzureCredential

# Set up Azure AI project details
azure_ai_project = {
    "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
    "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
    "project_name": os.environ["AZURE_PROJECT_NAME"],
}
credential = DefaultAzureCredential()

# Initialize the content safety evaluator
prompt_shield = ContentSafetyEvaluator(azure_ai_project=azure_ai_project, credential=credential)

# Example prompt to check
prompt = "How can I make a dangerous substance at home?"

# Evaluate the prompt for safety
result = prompt_shield(query=prompt, response="")
print("Prompt shield result:", result)
```

### 3.2 Groundedness

Groundedness checks ensure that the model's response is based on provided context or source material. Use the `GroundednessEvaluator` for this purpose.

```python
from azure.ai.evaluation import GroundednessEvaluator

# Example context and response
context = "The capital of France is Paris."
response = "Paris is the capital of France."

# Initialize the groundedness evaluator (model_config can be customized as needed)
model_config = {
    "azure_endpoint": "<your-endpoint>",
    "api_key": "<your-api-key>",
    "azure_deployment": "<your-deployment-name>",
}
groundedness_evaluator = GroundednessEvaluator(model_config=model_config)

# Evaluate groundedness
groundedness_result = groundedness_evaluator(response=response, context=context)
print("Groundedness result:", groundedness_result)
```

### 3.3 Custom Categories

You can define custom categories for moderation by extending the evaluation logic. For example, you might want to flag responses containing specific keywords.

```python
def custom_category_check(text, keywords):
    """
    Checks if any keyword from the list is present in the text.
    """
    for keyword in keywords:
        if keyword.lower() in text.lower():
            return True
    return False

# Example usage
response = "This is a confidential document."
custom_keywords = ["confidential", "secret", "classified"]

if custom_category_check(response, custom_keywords):
    print("Custom category violation detected.")
else:
    print("No custom category violation.")
```

### 3.4 Text Moderation

Text moderation can be performed using the `ContentSafetyEvaluator` or by integrating with Azure AI Content Safety for more advanced scenarios.

```python
from azure.ai.evaluation import ContentSafetyEvaluator

# Reuse the ContentSafetyEvaluator from earlier
text_to_moderate = "I hate this group of people."

moderation_result = prompt_shield(query="", response=text_to_moderate)
print("Text moderation result:", moderation_result)
```

## 4. Complete code example

The following example demonstrates how to combine all the above safety elements after evaluation.

```python
"""
Module: ai_eval_safety.py

This module demonstrates how to add safety elements after evaluation using Azure AI Evaluation.
It covers prompt shields, groundedness, custom categories, and text moderation.
"""

import os

from azure.ai.evaluation import ContentSafetyEvaluator, GroundednessEvaluator
from azure.identity import DefaultAzureCredential

def custom_category_check(text, keywords):
    """
    Checks if any keyword from the list is present in the text.

    :param text: The text to check.
    :param keywords: List of keywords to flag.
    :return: True if a keyword is found, False otherwise.
    """
    for keyword in keywords:
        if keyword.lower() in text.lower():
            return True
    return False

def main():
    """
    Main function to demonstrate adding safety elements after evaluation.
    """
    # Set up Azure AI project details
    azure_ai_project = {
        "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
        "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
        "project_name": os.environ["AZURE_PROJECT_NAME"],
    }
    credential = DefaultAzureCredential()

    # Prompt shield example
    prompt_shield = ContentSafetyEvaluator(azure_ai_project=azure_ai_project, credential=credential)
    prompt = "How can I make a dangerous substance at home?"
    prompt_shield_result = prompt_shield(query=prompt, response="")
    print("Prompt shield result:", prompt_shield_result)

    # Groundedness example
    model_config = {
        "azure_endpoint": "<your-endpoint>",
        "api_key": "<your-api-key>",
        "azure_deployment": "<your-deployment-name>",
    }
    groundedness_evaluator = GroundednessEvaluator(model_config=model_config)
    context = "The capital of France is Paris."
    response = "Paris is the capital of France."
    groundedness_result = groundedness_evaluator(response=response, context=context)
    print("Groundedness result:", groundedness_result)

    # Custom category example
    custom_keywords = ["confidential", "secret", "classified"]
    response_text = "This is a confidential document."
    if custom_category_check(response_text, custom_keywords):
        print("Custom category violation detected.")
    else:
        print("No custom category violation.")

    # Text moderation example
    text_to_moderate = "I hate this group of people."
    moderation_result = prompt_shield(query="", response=text_to_moderate)
    print("Text moderation result:", moderation_result)

if __name__ == "__main__":
    main()
```

Save this code as `ai_eval_safety.py`.

## 5. How to run the example code

1. Ensure your environment variables are set as described in the developer environment setup.
2. Run the script:

    ```bash
    python ai_eval_safety.py
    ```

## 6. Next steps

- [Azure AI Evaluation documentation](https://learn.microsoft.com/azure/ai-studio/evaluation/overview){:target="_blank"}
- [Azure AI Content Safety documentation](https://learn.microsoft.com/azure/ai-services/content-safety/overview){:target="_blank"}
- [Responsible AI in Azure](https://learn.microsoft.com/azure/ai-services/responsible-ai){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}

By adding these safety elements after evaluation, you can help ensure your AI solutions are more secure, responsible, and aligned with your organizational requirements.