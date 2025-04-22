# Generate a Sales by Region Pie Chart Using Code Interpreter in Azure AI Foundry

This guide shows you how to use the Code Interpreter tool in Azure AI Foundry Agents to generate a pie chart of sales by region using provided data. You will upload a CSV file with your sales data, create an agent with the Code Interpreter tool, and request a pie chart.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Introduction

You will create a CSV file with sales data by region, upload it to your Azure AI Foundry project, and use an agent with the Code Interpreter tool to generate a pie chart. The agent will process your request and return the chart as an image file.

## 2. Environment Setup

Follow the steps for your operating system to set up a virtual environment, install required libraries, and set environment variables.

=== "Windows"
    1. Open **Command Prompt**.
    2. Create and activate a virtual environment:
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```
    3. Install required libraries:
        ```cmd
        pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0
        ```
    4. Set environment variables:
        ```cmd
        set PROJECT_CONNECTION_STRING=<your-azure-ai-foundry-connection-string>
        set MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
        ```

=== "Linux/macOS"
    1. Open **Terminal**.
    2. Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    3. Install required libraries:
        ```bash
        pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0
        ```
    4. Set environment variables:
        ```bash
        export PROJECT_CONNECTION_STRING=<your-azure-ai-foundry-connection-string>
        export MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
        ```

## 3. Main Code Components

### 3.1 Prepare the Sales Data CSV

Create a CSV file named `sales_by_region.csv` with the following content:

```csv
Region,Sales
Europe,120000
China,150000
```

### 3.2 Upload the File and Create the Agent

This section uploads the CSV file, creates an agent with the Code Interpreter tool, and sends a request to generate a pie chart.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose, MessageRole
from azure.identity import DefaultAzureCredential
from pathlib import Path

# Initialize the AI Project client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    # Upload the sales data CSV file
    file = project_client.agents.upload_file_and_poll(
        file_path="sales_by_region.csv",
        purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded file, file ID: {file.id}")

    # Create the Code Interpreter tool with the uploaded file
    code_interpreter = CodeInterpreterTool(file_ids=[file.id])

    # Create an agent with the Code Interpreter tool
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="sales-assistant",
        instructions="You are a helpful assistant.",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")

    # Create a new thread for the conversation
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Send a message to the agent requesting a pie chart
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Generate a sales by region pie chart using the uploaded CSV file."
    )
    print(f"Created message, message ID: {message.id}")

    # Run the agent to process the request
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    # Download and save the generated image file(s)
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

#### Explanation

- The code uploads your CSV file to the project.
- It creates an agent with the Code Interpreter tool, referencing the uploaded file.
- It sends a message to the agent to generate a pie chart.
- The agent processes the request and returns an image file, which is saved locally.
- The code cleans up by deleting the file and agent.

## 4. Complete Code Example

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose, MessageRole
from azure.identity import DefaultAzureCredential
from pathlib import Path

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    file = project_client.agents.upload_file_and_poll(
        file_path="sales_by_region.csv",
        purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded file, file ID: {file.id}")

    code_interpreter = CodeInterpreterTool(file_ids=[file.id])

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

    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Generate a sales by region pie chart using the uploaded CSV file."
    )
    print(f"Created message, message ID: {message.id}")

    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    messages = project_client.agents.list_messages(thread_id=thread.id)
    for image_content in messages.image_contents:
        file_id = image_content.image_file.file_id
        file_name = f"{file_id}_sales_pie_chart.png"
        project_client.agents.save_file(file_id=file_id, file_name=file_name)
        print(f"Saved pie chart image to: {Path.cwd() / file_name}")

    project_client.agents.delete_file(file.id)
    project_client.agents.delete_agent(agent.id)
```

## 5. How to Run the Example

1. Save your sales data as `sales_by_region.csv` in your working directory.
2. Save the code above as `generate_sales_pie_chart.py`.
3. Ensure your environment variables are set and your virtual environment is activated.
4. Run the script:
    ```bash
    python generate_sales_pie_chart.py
    ```
5. The generated pie chart image will be saved in your current directory.

## 6. Next Steps

- Explore additional [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-services/foundry/){:target="_blank"}.
- Try using different datasets or chart types.
- Integrate the agent workflow into your applications.

---

**Related resources:**
- [Azure AI Projects Python SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects){:target="_blank"}
- [Azure AI Foundry quickstart](https://learn.microsoft.com/azure/ai-services/foundry/quickstart){:target="_blank"}