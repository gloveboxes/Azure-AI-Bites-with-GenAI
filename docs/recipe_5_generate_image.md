# Generate a Sales by Region Pie Chart Using Code Interpreter in Azure AI Foundry

This guide shows you how to use the Code Interpreter tool with Azure AI Foundry Agents to generate a pie chart of sales by region from provided data.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services (project and model deployment)

## Introduction

You will upload a CSV file containing sales data by region, create an agent with the Code Interpreter tool, and ask the agent to generate a pie chart. The agent will process your request and return the chart as an image file.

## 1. Environment Setup

Follow these steps to set up your Python environment and required libraries.

=== "Windows"
    1. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    2. Install required libraries:
        ```cmd
        pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0 azure-core==1.33.0
        ```
    3. Set environment variables:
        ```cmd
        set PROJECT_CONNECTION_STRING=<your-project-connection-string>
        set MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
        ```

=== "Linux/macOS"
    1. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    2. Install required libraries:
        ```bash
        pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0 azure-core==1.33.0
        ```
    3. Set environment variables:
        ```bash
        export PROJECT_CONNECTION_STRING=<your-project-connection-string>
        export MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
        ```

## 2. Main Code Components

### a. Prepare the Data

Create a CSV file named `sales_by_region.csv` with the following content:

```csv
Region,Sales
Europe,120000
China,150000
```

### b. Upload the File and Create the Agent

This component uploads the CSV file and creates an agent with the Code Interpreter tool.

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose
from azure.identity import DefaultAzureCredential
import os

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    # Upload the CSV file
    file = project_client.agents.upload_file_and_poll(
        file_path="sales_by_region.csv", purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded file, file ID: {file.id}")

    # Create the Code Interpreter tool
    code_interpreter = CodeInterpreterTool(file_ids=[file.id])

    # Create the agent
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="sales-assistant",
        instructions="You are a helpful assistant.",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")
```

### c. Create a Thread, Send the Request, and Process the Run

This component creates a conversation thread, sends a message to generate the pie chart, and processes the run.

```python
    # Create a thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Send the user message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Generate a sales by region pie chart using the uploaded CSV file.",
    )
    print(f"Created message, message ID: {message.id}")

    # Run the agent
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")
```

### d. Download and Save the Generated Chart

This component retrieves the generated image file and saves it locally.

```python
    # List messages and download image file(s)
    messages = project_client.agents.list_messages(thread_id=thread.id)
    for image_content in messages.image_contents:
        file_id = image_content.image_file.file_id
        file_name = f"{file_id}_sales_pie_chart.png"
        project_client.agents.save_file(file_id=file_id, file_name=file_name)
        print(f"Saved image file to: {file_name}")
```

### e. Clean Up Resources

Delete the agent and uploaded file to avoid unnecessary resource usage.

```python
    project_client.agents.delete_file(file.id)
    print("Deleted file")

    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

## 3. Complete Code Example

Below is the complete code example. Make sure the `sales_by_region.csv` file is in your working directory.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    # Upload the CSV file
    file = project_client.agents.upload_file_and_poll(
        file_path="sales_by_region.csv", purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded file, file ID: {file.id}")

    # Create the Code Interpreter tool
    code_interpreter = CodeInterpreterTool(file_ids=[file.id])

    # Create the agent
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="sales-assistant",
        instructions="You are a helpful assistant.",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")

    # Create a thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Send the user message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Generate a sales by region pie chart using the uploaded CSV file.",
    )
    print(f"Created message, message ID: {message.id}")

    # Run the agent
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    # List messages and download image file(s)
    messages = project_client.agents.list_messages(thread_id=thread.id)
    for image_content in messages.image_contents:
        file_id = image_content.image_file.file_id
        file_name = f"{file_id}_sales_pie_chart.png"
        project_client.agents.save_file(file_id=file_id, file_name=file_name)
        print(f"Saved image file to: {file_name}")

    # Clean up
    project_client.agents.delete_file(file.id)
    print("Deleted file")

    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

## 4. How to Run the Example

1. Prepare the `sales_by_region.csv` file as shown above.
2. Set the required environment variables for your Azure AI Foundry project and model deployment.
3. Run the script:
    ```bash
    python <your_script_name>.py
    ```
4. After completion, check your working directory for the generated pie chart image file.

## 5. Next Steps

- Explore more agent tools and capabilities in [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"}.
- Learn how to [add more data sources or tools to your agent](https://learn.microsoft.com/azure/ai-foundry/how-to/agents-overview){:target="_blank"}.
- Review [Code Interpreter tool documentation](https://learn.microsoft.com/azure/ai-foundry/how-to/agents-code-interpreter){:target="_blank"} for advanced scenarios.