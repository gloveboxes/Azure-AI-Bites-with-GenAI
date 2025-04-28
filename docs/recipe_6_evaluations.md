# Evaluate Your Agents with Azure AI Evaluation

## Introduction

This article demonstrates how to evaluate your agents using the Azure AI Evaluation library. You will learn how to generate an evaluation dataset, run a local evaluation, and perform an online evaluation. The goal is to help you assess the quality and safety of your agent's responses using built-in evaluators.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system to set up your environment.

=== "Windows (PowerShell)"
    1. Open **PowerShell**.
    2. Create a project folder:
        ```powershell
        mkdir agent-eval-sample
        cd agent-eval-sample
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
    5. Set environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:AZURE_OPENAI_ENDPOINT="<your-aoai-endpoint>"
        $env:AZURE_OPENAI_KEY="<your-aoai-key>"
        $env:AZURE_OPENAI_DEPLOYMENT="<your-aoai-deployment>"
        $env:AZURE_SUBSCRIPTION_ID="<your-subscription-id>"
        $env:AZURE_RESOURCE_GROUP_NAME="<your-resource-group>"
        $env:AZURE_PROJECT_NAME="<your-project-name>"
        ```

=== "Linux/macOS"
    1. Open a terminal.
    2. Create a project folder:
        ```bash
        mkdir agent-eval-sample
        cd agent-eval-sample
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
    5. Set environment variables. Replace the placeholders with the actual values:
        ```bash
        export AZURE_OPENAI_ENDPOINT="<your-aoai-endpoint>"
        export AZURE_OPENAI_KEY="<your-aoai-key>"
        export AZURE_OPENAI_DEPLOYMENT="<your-aoai-deployment>"
        export AZURE_SUBSCRIPTION_ID="<your-subscription-id>"
        export AZURE_RESOURCE_GROUP_NAME="<your-resource-group>"
        export AZURE_PROJECT_NAME="<your-project-name>"
        ```

## 2. Main code components

### 2.1 Generate an evaluation dataset

This step shows how to create a simple evaluation dataset in JSONL format. Each line is a JSON object representing a test case.

```python
import json

eval_data = [
    {
        "query": "What is the capital of France?",
        "context": "France is a country in Europe.",
        "response": "Paris is the capital of France."
    },
    {
        "query": "What is the capital of Japan?",
        "context": "Japan is a country in Asia.",
        "response": "Tokyo is the capital of Japan."
    }
]

with open("eval_dataset.jsonl", "w") as f:
    for item in eval_data:
        f.write(json.dumps(item) + "\n")
```

### 2.2 Local evaluation run

This example demonstrates how to run a local evaluation using built-in evaluators. The evaluation is performed on the dataset you created.

```python
import os
from azure.ai.evaluation import evaluate, RelevanceEvaluator, CoherenceEvaluator

model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "azure_deployment": os.environ["AZURE_OPENAI_DEPLOYMENT"],
}

evaluate(
    data="eval_dataset.jsonl",
    evaluators={
        "relevance": RelevanceEvaluator(model_config=model_config),
        "coherence": CoherenceEvaluator(model_config=model_config),
    },
    evaluator_config={
        "relevance": {
            "column_mapping": {
                "response": "${data.response}",
                "context": "${data.context}",
                "query": "${data.query}",
            }
        },
        "coherence": {
            "column_mapping": {
                "response": "${data.response}",
                "query": "${data.query}",
            }
        }
    }
)
```

### 2.3 Online evaluation run

This example shows how to run an online evaluation using Azure AI Project resources. You need to provide your Azure subscription, resource group, and project name.

```python
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import ContentSafetyEvaluator

azure_ai_project = {
    "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
    "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
    "project_name": os.environ["AZURE_PROJECT_NAME"],
}
credential = DefaultAzureCredential()

content_safety_eval = ContentSafetyEvaluator(
    azure_ai_project=azure_ai_project,
    credential=credential
)

result = content_safety_eval(
    query="What is the capital of France?",
    response="Paris"
)
print(result)
```

## 3. Complete code example

The following script combines all the steps above. Save this as `evaluate_agent_example.py`.

```python
import os
import json
from azure.ai.evaluation import evaluate, RelevanceEvaluator, CoherenceEvaluator, ContentSafetyEvaluator
from azure.identity import DefaultAzureCredential

# Step 1: Generate evaluation dataset
eval_data = [
    {
        "query": "What is the capital of France?",
        "context": "France is a country in Europe.",
        "response": "Paris is the capital of France."
    },
    {
        "query": "What is the capital of Japan?",
        "context": "Japan is a country in Asia.",
        "response": "Tokyo is the capital of Japan."
    }
]
with open("eval_dataset.jsonl", "w") as f:
    for item in eval_data:
        f.write(json.dumps(item) + "\n")

# Step 2: Local evaluation run
model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "azure_deployment": os.environ["AZURE_OPENAI_DEPLOYMENT"],
}
evaluate(
    data="eval_dataset.jsonl",
    evaluators={
        "relevance": RelevanceEvaluator(model_config=model_config),
        "coherence": CoherenceEvaluator(model_config=model_config),
    },
    evaluator_config={
        "relevance": {
            "column_mapping": {
                "response": "${data.response}",
                "context": "${data.context}",
                "query": "${data.query}",
            }
        },
        "coherence": {
            "column_mapping": {
                "response": "${data.response}",
                "query": "${data.query}",
            }
        }
    }
)

# Step 3: Online evaluation run
azure_ai_project = {
    "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
    "resource_group_name": os.environ["AZURE_RESOURCE_GROUP_NAME"],
    "project_name": os.environ["AZURE_PROJECT_NAME"],
}
credential = DefaultAzureCredential()
content_safety_eval = ContentSafetyEvaluator(
    azure_ai_project=azure_ai_project,
    credential=credential
)
result = content_safety_eval(
    query="What is the capital of France?",
    response="Paris"
)
print(result)
```

**Save this file as** `evaluate_agent_example.py`.

## 4. How to run the example code

1. Ensure your environment variables are set as described in the setup section.
2. Run the script:
    ```bash
    python evaluate_agent_example.py
    ```

## 5. Next steps

- [Azure AI Evaluation documentation](https://learn.microsoft.com/azure/ai-services/foundry/how-to/evaluation-overview){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-services/foundry/){:target="_blank"}
- [Azure AI Evaluation Python SDK Reference](https://pypi.org/project/azure-ai-evaluation/){:target="_blank"}
- [Evaluate generative AI models](https://learn.microsoft.com/azure/ai-services/foundry/how-to/evaluation-overview){:target="_blank"}