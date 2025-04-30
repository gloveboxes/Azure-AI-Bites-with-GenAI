# Evaluate Your Agents with Azure AI Evaluation

## Introduction

This article demonstrates how to evaluate your Azure AI Agents using the `azure-ai-evaluation` library. You will learn how to generate an evaluation dataset, run a local evaluation, and perform an online evaluation. The goal is to help you assess the quality and safety of your agent's responses using built-in evaluators.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Authentication

Azure AI Evaluation supports both local and online evaluation. For online evaluation, you need to authenticate with your Azure AI Foundry project using Microsoft Entra ID.

Azure AI Foundry is a platform for building, deploying, and evaluating AI models and agents. It provides tools for managing projects, running evaluations, and integrating with Azure resources.

To authenticate:

1. Ensure you have an Azure subscription and an Azure AI Foundry project.
2. Install the Azure CLI and run `az login` to authenticate your account.
3. Use `DefaultAzureCredential` in your code to access Azure resources.

## 2. Developer environment setup

Select your preferred operating system and follow the steps below.

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a project folder:
        ```powershell
        mkdir agent-eval-demo
        cd agent-eval-demo
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
        mkdir agent-eval-demo
        cd agent-eval-demo
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

### 3.1 Generate an Evaluation Dataset

You can create a simple evaluation dataset as a JSONL file. Each line represents a test case with a user query and the expected response.

```python
import json

# Example dataset with user queries and expected responses
eval_data = [
    {"query": "What is the capital of France?", "response": "Paris"},
    {"query": "What is 2 + 2?", "response": "4"},
]

with open("eval_dataset.jsonl", "w") as f:
    for item in eval_data:
        f.write(json.dumps(item) + "\n")
```

### 3.2 Local Evaluation Run

A local evaluation run uses built-in evaluators to score your agent's responses. This does not require Azure resources.

```python
from azure.ai.evaluation import evaluate, CoherenceEvaluator, RelevanceEvaluator

# Run local evaluation using the dataset
evaluate(
    data="eval_dataset.jsonl",
    evaluators={
        "coherence": CoherenceEvaluator(),
        "relevance": RelevanceEvaluator(),
    },
    evaluator_config={
        "coherence": {
            "column_mapping": {
                "response": "${data.response}",
                "query": "${data.query}",
            },
        },
        "relevance": {
            "column_mapping": {
                "response": "${data.response}",
                "query": "${data.query}",
            },
        },
    },
)
```

### 3.3 Online Evaluation Run

An online evaluation run uses Azure AI Foundry resources and can leverage additional evaluators, such as content safety. You must authenticate using `DefaultAzureCredential`.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import ContentSafetyEvaluator, evaluate

azure_ai_project = {
    "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
    "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
    "project_name": os.environ["AZURE_PROJECT_NAME"],
}

credential = DefaultAzureCredential()

# Run online evaluation using the dataset and content safety evaluator
evaluate(
    data="eval_dataset.jsonl",
    evaluators={
        "content_safety": ContentSafetyEvaluator(azure_ai_project=azure_ai_project, credential=credential),
    },
    evaluator_config={
        "content_safety": {
            "column_mapping": {
                "response": "${data.response}",
                "query": "${data.query}",
            },
        },
    },
)
```

## 4. Complete code example

The following script demonstrates the full workflow: generating a dataset, running a local evaluation, and running an online evaluation.

```python
"""
Evaluate your Azure AI Agent: generate dataset, run local and online evaluation.

This script demonstrates:
- How to generate a simple evaluation dataset
- How to run a local evaluation
- How to run an online evaluation using Azure AI Foundry

Replace the environment variable placeholders with your actual Azure values.
"""

import json
import os

from azure.ai.evaluation import evaluate, CoherenceEvaluator, RelevanceEvaluator, ContentSafetyEvaluator
from azure.identity import DefaultAzureCredential

def generate_eval_dataset(filename: str):
    """
    Generate a simple evaluation dataset as a JSONL file.
    """
    eval_data = [
        {"query": "What is the capital of France?", "response": "Paris"},
        {"query": "What is 2 + 2?", "response": "4"},
    ]
    with open(filename, "w") as f:
        for item in eval_data:
            f.write(json.dumps(item) + "\n")

def run_local_eval(filename: str):
    """
    Run a local evaluation using built-in evaluators.
    """
    evaluate(
        data=filename,
        evaluators={
            "coherence": CoherenceEvaluator(),
            "relevance": RelevanceEvaluator(),
        },
        evaluator_config={
            "coherence": {
                "column_mapping": {
                    "response": "${data.response}",
                    "query": "${data.query}",
                },
            },
            "relevance": {
                "column_mapping": {
                    "response": "${data.response}",
                    "query": "${data.query}",
                },
            },
        },
    )

def run_online_eval(filename: str):
    """
    Run an online evaluation using Azure AI Foundry and content safety evaluator.
    """
    azure_ai_project = {
        "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
        "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
        "project_name": os.environ["AZURE_PROJECT_NAME"],
    }
    credential = DefaultAzureCredential()
    evaluate(
        data=filename,
        evaluators={
            "content_safety": ContentSafetyEvaluator(azure_ai_project=azure_ai_project, credential=credential),
        },
        evaluator_config={
            "content_safety": {
                "column_mapping": {
                    "response": "${data.response}",
                    "query": "${data.query}",
                },
            },
        },
    )

if __name__ == "__main__":
    """
    Main entry point for agent evaluation.
    """
    dataset_file = "eval_dataset.jsonl"
    print("Generating evaluation dataset...")
    generate_eval_dataset(dataset_file)
    print("Running local evaluation...")
    run_local_eval(dataset_file)
    print("Running online evaluation...")
    run_online_eval(dataset_file)
    print("Evaluation complete.")
```

Save this code as `agent_eval_example.py`.

## 5. How to run the example code

1. Ensure your environment variables are set as described in the developer setup.
2. Run the script:

    ```bash
    python agent_eval_example.py
    ```

The script will generate a dataset, run a local evaluation, and then run an online evaluation using Azure AI Foundry.

## 6. Next steps

- Learn more about [Azure AI Evaluation documentation](https://aka.ms/azure-ai-evaluation){:target="_blank"}
- Explore [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- Review [Azure AI Evaluation samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation/samples){:target="_blank"}
- See [How to evaluate generative AI models](https://learn.microsoft.com/azure/ai-studio/how-to/evaluate-models){:target="_blank"}