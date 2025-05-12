# Evaluate Your Azure AI Agents: Generate Dataset, Local Evaluation, and Online Evaluation

## Introduction

This article demonstrates how to evaluate your Azure AI Agents using the `azure-ai-evaluation` library. You will learn how to generate an evaluation dataset, perform a local evaluation run, and execute an online evaluation run. The goal is to help you assess the quality and safety of your agent's responses using both offline and online evaluation workflows.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services with an existing project and agent deployment

## 1. Authentication

This example uses a **project connection string** and **Microsoft Entra ID authentication**.

- **Project Connection String**: This string connects your code to a specific Azure AI Foundry project. You can find it in the Azure AI Foundry portal by selecting your project and copying the connection string from the **Overview** tab under **Project details**.
- **Microsoft Entra ID Authentication**: This method uses your Azure identity to securely access Azure resources. You must have the [Azure CLI installed](https://learn.microsoft.com/cli/azure/install-azure-cli){:target="_blank"} and be signed in with `az login`.

**Steps:**

1. Go to the Azure AI Foundry portal and select your project.
2. Copy the **Project Connection String** from the **Overview** tab.
3. Ensure you are signed in to Azure CLI with `az login`.
4. Set the following environment variables in your terminal:
   
   - `PROJECT_CONNECTION_STRING` — your project connection string
   - `MODEL_DEPLOYMENT_NAME` — the name of your deployed agent/model

## 2. Developer environment setup

Select your preferred operating system:

=== "Windows (PowerShell)"

    ```powershell
    # Open a terminal
    mkdir agent-eval-sample
    cd agent-eval-sample

    # Set up a virtual environment
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

    # Install required libraries
    pip install azure-ai-evaluation==1.5.0 azure-ai-projects==1.0.0b9 azure-identity==1.21.0

    # Set environment variables (replace the placeholders with the actual values)
    $env:PROJECT_CONNECTION_STRING="<your-project-connection-string>"
    $env:MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
    ```

=== "Linux/macOS"

    ```bash
    # Open a terminal
    mkdir agent-eval-sample
    cd agent-eval-sample

    # Set up a virtual environment
    python3 -m venv .venv
    source .venv/bin/activate

    # Install required libraries
    pip install azure-ai-evaluation==1.5.0 azure-ai-projects==1.0.0b9 azure-identity==1.21.0

    # Set environment variables (replace the placeholders with the actual values)
    export PROJECT_CONNECTION_STRING="<your-project-connection-string>"
    export MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
    ```

Replace the placeholders with the actual values from your Azure AI Foundry project.

## 3. Main code components

### 3.1 Generate an Evaluation Dataset

This code shows how to generate a synthetic evaluation dataset for your agent using the `azure-ai-evaluation` library.

```python
import os

from azure.ai.evaluation import generate_eval_dataset
from azure.identity import DefaultAzureCredential

def generate_dataset():
    """
    Generate a synthetic evaluation dataset for the agent.
    """
    # Use the project connection string and Entra ID authentication
    project_connection_string = os.environ["PROJECT_CONNECTION_STRING"]
    deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]

    # Generate a dataset with 5 samples
    generate_eval_dataset(
        project_connection_string=project_connection_string,
        deployment_name=deployment_name,
        credential=DefaultAzureCredential(),
        output_path="agent_eval_dataset.jsonl",
        num_samples=5,
    )
    print("Evaluation dataset generated: agent_eval_dataset.jsonl")
```

### 3.2 Local Evaluation Run

This code demonstrates how to run a local evaluation using the generated dataset. The evaluation is performed locally without sending data to Azure.

```python
from azure.ai.evaluation import evaluate, RelevanceEvaluator, CoherenceEvaluator

def local_eval_run():
    """
    Perform a local evaluation run using the generated dataset.
    """
    dataset_path = "agent_eval_dataset.jsonl"

    evaluate(
        data=dataset_path,
        evaluators={
            "relevance": RelevanceEvaluator(),
            "coherence": CoherenceEvaluator(),
        },
        evaluator_config={
            "relevance": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}",
                }
            },
            "coherence": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}",
                }
            },
        },
        output_path="agent_local_eval_results.jsonl",
    )
    print("Local evaluation completed: agent_local_eval_results.jsonl")
```

### 3.3 Online Evaluation Run

This code shows how to run an online evaluation, which uses Azure-hosted evaluation services for more advanced metrics and safety checks.

```python
from azure.ai.evaluation import evaluate, ContentSafetyEvaluator

def online_eval_run():
    """
    Perform an online evaluation run using Azure-hosted evaluation services.
    """
    from azure.identity import DefaultAzureCredential

    dataset_path = "agent_eval_dataset.jsonl"
    project_connection_string = os.environ["PROJECT_CONNECTION_STRING"]

    evaluate(
        data=dataset_path,
        evaluators={
            "content_safety": ContentSafetyEvaluator(
                project_connection_string=project_connection_string,
                credential=DefaultAzureCredential(),
            ),
        },
        evaluator_config={
            "content_safety": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}",
                }
            },
        },
        output_path="agent_online_eval_results.jsonl",
    )
    print("Online evaluation completed: agent_online_eval_results.jsonl")
```

## 4. Complete code

Below is the complete example. Save this as `agent_evaluation_example.py`.

```python
"""
Evaluate your Azure AI Agent: Generate dataset, local evaluation, and online evaluation.

This script demonstrates how to:
- Generate a synthetic evaluation dataset for your agent
- Run a local evaluation
- Run an online evaluation using Azure-hosted services

Authentication uses a project connection string and Microsoft Entra ID.
"""

import os

from azure.ai.evaluation import (
    generate_eval_dataset,
    evaluate,
    RelevanceEvaluator,
    CoherenceEvaluator,
    ContentSafetyEvaluator,
)
from azure.identity import DefaultAzureCredential

def generate_dataset():
    """
    Generate a synthetic evaluation dataset for the agent.
    """
    project_connection_string = os.environ["PROJECT_CONNECTION_STRING"]
    deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]

    generate_eval_dataset(
        project_connection_string=project_connection_string,
        deployment_name=deployment_name,
        credential=DefaultAzureCredential(),
        output_path="agent_eval_dataset.jsonl",
        num_samples=5,
    )
    print("Evaluation dataset generated: agent_eval_dataset.jsonl")

def local_eval_run():
    """
    Perform a local evaluation run using the generated dataset.
    """
    dataset_path = "agent_eval_dataset.jsonl"

    evaluate(
        data=dataset_path,
        evaluators={
            "relevance": RelevanceEvaluator(),
            "coherence": CoherenceEvaluator(),
        },
        evaluator_config={
            "relevance": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}",
                }
            },
            "coherence": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}",
                }
            },
        },
        output_path="agent_local_eval_results.jsonl",
    )
    print("Local evaluation completed: agent_local_eval_results.jsonl")

def online_eval_run():
    """
    Perform an online evaluation run using Azure-hosted evaluation services.
    """
    dataset_path = "agent_eval_dataset.jsonl"
    project_connection_string = os.environ["PROJECT_CONNECTION_STRING"]

    evaluate(
        data=dataset_path,
        evaluators={
            "content_safety": ContentSafetyEvaluator(
                project_connection_string=project_connection_string,
                credential=DefaultAzureCredential(),
            ),
        },
        evaluator_config={
            "content_safety": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}",
                }
            },
        },
        output_path="agent_online_eval_results.jsonl",
    )
    print("Online evaluation completed: agent_online_eval_results.jsonl")

if __name__ == "__main__":
    generate_dataset()
    local_eval_run()
    online_eval_run()
```

## 5. How to run the example code

1. Ensure your environment variables are set as described in the **Developer environment setup** section.
2. Save the complete code as `agent_evaluation_example.py`.
3. Run the script:

   ```bash
   python agent_evaluation_example.py
   ```

4. After execution, you will find the following files in your working directory:
   - `agent_eval_dataset.jsonl` — the generated evaluation dataset
   - `agent_local_eval_results.jsonl` — results from the local evaluation
   - `agent_online_eval_results.jsonl` — results from the online evaluation

## 6. Next steps

- [Azure AI Evaluation documentation](https://aka.ms/azure-ai-evaluation-docs){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- [Evaluate generative AI models and agents](https://learn.microsoft.com/azure/ai-foundry/how-to/evaluate-models-agents){:target="_blank"}
- [Azure AI Evaluation Python SDK reference](https://aka.ms/azsdk/azure-ai-evaluation/python/reference){:target="_blank"}
- [Azure AI Foundry Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-evaluation/samples){:target="_blank"}
