# Generate a Sales by Region Pie Chart Using Code Interpreter in Azure AI Foundry

## Introduction

This guide shows you how to use the Code Interpreter tool in Azure AI Foundry Agents to generate a pie chart of sales by region from a CSV file. You will upload a CSV file containing sales data, create an agent with the Code Interpreter tool, and request a pie chart visualization.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your environment.

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a new project folder:
        ```powershell
        mkdir foundry-code-interpreter-demo
        cd foundry-code-interpreter-demo
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
        mkdir foundry-code-interpreter-demo
        cd foundry-code-interpreter-demo
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

## 2. Prepare the sales data CSV file

Create a file named `sales_data.csv` in your project folder with the following content:

```csv
Region,SalesUSD
Europe,120000
China,150000
```

## 3. Main code components

### 3.1 Upload the CSV file and create the Code Interpreter tool

This part uploads your CSV file to Azure AI Foundry and prepares the Code Interpreter tool to use the file.

```python
file = project_client.agents.upload_file_and_poll(
    file_path="sales_data.csv", purpose=FilePurpose.AGENTS
)
code_interpreter = CodeInterpreterTool(file_ids=[file.id])
```

### 3.2 Create an agent with the Code Interpreter tool

This code creates an agent that can use the Code Interpreter tool and access your uploaded file.

```python
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="sales-assistant",
    instructions="You are a helpful assistant.",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
```

### 3.3 Create a thread and send a message to generate the pie chart

This section creates a conversation thread and sends a message instructing the agent to generate a pie chart.

```python
thread = project_client.agents.create_thread()
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Generate a sales by region pie chart using the uploaded sales_data.csv file.",
)
```

### 3.4 Run the agent and retrieve the result

This part runs the agent, checks the run status, and retrieves the generated chart file.

```python
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
messages = project_client.agents.list_messages(thread_id=thread.id)

for image_content in messages.image_contents:
    file_id = image_content.image_file.file_id
    file_name = f"{file_id}_sales_pie_chart.png"
    project_client.agents.save_file(file_id=file_id, file_name=file_name)
    print(f"Saved pie chart image to: {file_name}")
```

## 4. Complete code example

The following example combines all the steps. Save this code as `example.py` in your project folder.

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
    # Upload the sales data CSV file
    file = project_client.agents.upload_file_and_poll(
        file_path="sales_data.csv", purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded file, file ID: {file.id}")

    code_interpreter = CodeInterpreterTool(file_ids=[file.id])

    # Create agent with code interpreter tool
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="sales-assistant",
        instructions="You are a helpful assistant.",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")

    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Send a message to generate the pie chart
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Generate a sales by region pie chart using the uploaded sales_data.csv file.",
    )
    print(f"Created message, message ID: {message.id}")

    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Retrieve and save the generated pie chart image
    messages = project_client.agents.list_messages(thread_id=thread.id)
    for image_content in messages.image_contents:
        file_id = image_content.image_file.file_id
        file_name = f"{file_id}_sales_pie_chart.png"
        project_client.agents.save_file(file_id=file_id, file_name=file_name)
        print(f"Saved pie chart image to: {Path.cwd() / file_name}")

    project_client.agents.delete_file(file.id)
    print("Deleted file")
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

This script uploads your sales data, creates an agent, requests a pie chart, and saves the resulting image.

## 5. How to run the example code

1. Ensure your environment variables are set and your virtual environment is activated.
2. Place your `sales_data.csv` file in the project folder.
3. Run the script:

    ```bash
    python example.py
    ```

4. After the script completes, look for a file ending with `_sales_pie_chart.png` in your project folder. This file contains the generated pie chart.

## 6. Next steps

- Learn more about [Azure AI Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- Explore [Code Interpreter tool documentation](https://learn.microsoft.com/azure/ai-foundry/agents/code-interpreter){:target="_blank"}
- Review [Azure AI Foundry model catalog](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview){:target="_blank"}
- Try adding more regions or data to your CSV file and rerun the script to generate updated charts.