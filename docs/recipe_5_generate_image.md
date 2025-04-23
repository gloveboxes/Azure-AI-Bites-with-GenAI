# Generate a Sales by Region Pie Chart Using Code Interpreter in Azure AI Foundry

## Introduction

This guide shows you how to use the Code Interpreter tool in Azure AI Foundry Agents to generate a pie chart of sales by region. You will upload a CSV file containing sales data and instruct the agent to create a pie chart using the Code Interpreter.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Developer environment setup

Select your preferred operating system and follow the steps to set up your environment.

=== "Windows"

    1. Open **Command Prompt** or **PowerShell**.
    2. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    3. Install the required Python libraries:
        ```cmd
        pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0 azure-core==1.33.0
        ```
    4. Set the required environment variables. Replace the placeholders with the actual values:
        ```cmd
        set PROJECT_CONNECTION_STRING=<your-project-connection-string>
        set MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    3. Install the required Python libraries:
        ```bash
        pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0 azure-core==1.33.0
        ```
    4. Set the required environment variables. Replace the placeholders with the actual values:
        ```bash
        export PROJECT_CONNECTION_STRING=<your-project-connection-string>
        export MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
        ```

## 2. Main code components

### 2.1. Prepare the sales data CSV file

Create a file named `sales_data.csv` in your working directory with the following content:

```csv
Region,Sales
Europe,120000
China,150000
```

This file contains the sales data by region.

### 2.2. Upload the file and create an agent with Code Interpreter

This code uploads the CSV file to Azure AI Foundry, creates an agent with the Code Interpreter tool, and provides the file as a resource.

```python
file = project_client.agents.upload_file_and_poll(
    file_path="sales_data.csv", purpose=FilePurpose.AGENTS
)
code_interpreter = CodeInterpreterTool(file_ids=[file.id])
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="sales-assistant",
    instructions="You are a helpful assistant.",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
```

### 2.3. Create a thread and send a message to generate the pie chart

This code creates a conversation thread and sends a message instructing the agent to generate a pie chart.

```python
thread = project_client.agents.create_thread()
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Generate a sales by region pie chart using the uploaded sales_data.csv file.",
)
```

### 2.4. Run the agent and retrieve the result

This code runs the agent, retrieves the messages, and saves any generated image files.

```python
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
messages = project_client.agents.list_messages(thread_id=thread.id)

for image_content in messages.image_contents:
    file_id = image_content.image_file.file_id
    file_name = f"{file_id}_sales_pie_chart.png"
    project_client.agents.save_file(file_id=file_id, file_name=file_name)
    print(f"Saved pie chart image to: {file_name}")
```

## 3. Complete code example

The following script combines all the steps above. It uploads the sales data, creates an agent with Code Interpreter, sends the instruction, and saves the resulting pie chart.

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
        content="Generate a sales by region pie chart using the uploaded sales_data.csv file.",
    )
    print(f"Created message, message ID: {message.id}")

    # Run the agent and process the result
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

**Explanation:**  
This script uploads your sales data, creates an agent with the Code Interpreter, sends a request to generate a pie chart, and saves the resulting image file to your local directory.

## 4. How to run the example code

1. Create a file named `sales_data.csv` in your working directory with the following content:
    ```csv
    Region,Sales
    Europe,120000
    China,150000
    ```
2. Set the required environment variables as described in the setup section.
3. Run the script:
    ```bash
    python <your_script_name>.py
    ```
4. After the script completes, look for a file ending with `_sales_pie_chart.png` in your working directory. This file contains the generated pie chart.

## 5. Next steps

- Explore more about [Azure AI Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}
- Learn how to [add more tools and files to your agents](https://learn.microsoft.com/azure/ai-foundry/how-to/agents-overview){:target="_blank"}
- Review [Code Interpreter tool documentation](https://learn.microsoft.com/azure/ai-foundry/how-to/agents-code-interpreter){:target="_blank"}