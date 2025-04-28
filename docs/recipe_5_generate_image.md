# Generate a Sales by Region Pie Chart Using Code Interpreter in Azure AI Foundry

## Introduction

This guide shows you how to use the Code Interpreter tool in Azure AI Foundry Agents to generate a pie chart of sales by region from a CSV file. You will upload a sample sales data file, create an agent with the Code Interpreter, and request a pie chart visualization.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your environment.

=== "Windows (PowerShell)"

    1. Open **PowerShell**.
    2. Create a new project folder:
        ```powershell
        mkdir sales-piechart-demo
        cd sales-piechart-demo
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
        pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```powershell
        $env:PROJECT_CONNECTION_STRING="<your-project-connection-string>"
        $env:MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a new project folder:
        ```bash
        mkdir sales-piechart-demo
        cd sales-piechart-demo
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
        pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0
        ```
    6. Set up environment variables. Replace the placeholders with the actual values:
        ```bash
        export PROJECT_CONNECTION_STRING="<your-project-connection-string>"
        export MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
        ```

## 2. Prepare the sales data file

Create a CSV file named `sales_data.csv` with the following content:

```csv
Region,SalesUSD
Europe,120000
China,150000
```

Save this file in your project folder.

## 3. Main code components

### 3.1 Upload the sales data file

This part uploads your `sales_data.csv` file to Azure AI Foundry and prepares it for use with the agent.

```python
file = project_client.agents.upload_file_and_poll(
    file_path="sales_data.csv", purpose=FilePurpose.AGENTS
)
print(f"Uploaded file, file ID: {file.id}")
```

### 3.2 Create an agent with the Code Interpreter tool

This section creates an agent that can use the Code Interpreter tool and access your uploaded file.

```python
code_interpreter = CodeInterpreterTool(file_ids=[file.id])

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="sales-assistant",
    instructions="You are a helpful assistant.",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
print(f"Created agent, agent ID: {agent.id}")
```

### 3.3 Create a thread and send a message

This part creates a conversation thread and sends a request to generate a pie chart.

```python
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Generate a pie chart of sales by region using the uploaded sales_data.csv file.",
)
print(f"Created message, message ID: {message.id}")
```

### 3.4 Run the agent and retrieve the result

This section runs the agent and retrieves the generated chart.

```python
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

messages = project_client.agents.list_messages(thread_id=thread.id)
for image_content in messages.image_contents:
    file_id = image_content.image_file.file_id
    file_name = f"{file_id}_sales_pie_chart.png"
    project_client.agents.save_file(file_id=file_id, file_name=file_name)
    print(f"Saved pie chart image to: {file_name}")
```

### 3.5 Clean up resources

This part deletes the agent and uploaded file after the run.

```python
project_client.agents.delete_file(file.id)
project_client.agents.delete_agent(agent.id)
```

## 4. Complete code example

The following script combines all the steps above. Save this code as `example.py` in your project folder.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose, MessageRole
from azure.identity import DefaultAzureCredential
from pathlib import Path

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    # Upload the sales data file
    file = project_client.agents.upload_file_and_poll(
        file_path="sales_data.csv", purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded file, file ID: {file.id}")

    # Create agent with Code Interpreter tool
    code_interpreter = CodeInterpreterTool(file_ids=[file.id])
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="sales-assistant",
        instructions="You are a helpful assistant.",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")

    # Create a thread and send a message
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Generate a pie chart of sales by region using the uploaded sales_data.csv file.",
    )
    print(f"Created message, message ID: {message.id}")

    # Run the agent and retrieve the result
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    messages = project_client.agents.list_messages(thread_id=thread.id)
    for image_content in messages.image_contents:
        file_id = image_content.image_file.file_id
        file_name = f"{file_id}_sales_pie_chart.png"
        project_client.agents.save_file(file_id=file_id, file_name=file_name)
        print(f"Saved pie chart image to: {Path.cwd() / file_name}")

    # Clean up resources
    project_client.agents.delete_file(file.id)
    project_client.agents.delete_agent(agent.id)
```

This script uploads your sales data, creates an agent with the Code Interpreter, requests a pie chart, saves the resulting image, and cleans up resources.

## 5. How to run the example code

1. Ensure your environment variables are set and your virtual environment is activated.
2. Place your `sales_data.csv` file in the project folder.
3. Run the script:

    ```bash
    python example.py
    ```

4. After the script completes, look for a file named similar to `<file_id>_sales_pie_chart.png` in your project folder. This is your generated pie chart.

## 6. Next steps

- [Learn more about using the Code Interpreter tool in Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Explore the model catalog in Azure AI Foundry portal](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- [Azure AI Projects Python SDK reference](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects){:target="_blank"}