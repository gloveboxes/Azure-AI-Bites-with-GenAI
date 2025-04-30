# Generate a Sales by Region Pie Chart Using Code Interpreter

## Introduction

This guide shows you how to use the Code Interpreter tool in Azure AI Foundry Agents to generate a pie chart of sales by region. You will use a sample dataset with sales figures for Europe and China.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Authentication

Azure AI Foundry provides secure access to AI and data services. You will need to authenticate using your Azure AI Foundry project connection string and model deployment name.

1. Go to your Azure AI Foundry project in the portal.
2. Copy the **Project Connection String** from the **Overview** tab.
3. Copy the **Model Deployment Name** from the **Models + endpoints** tab.

## 2. Developer environment setup

Select your operating system and follow the steps below.

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a new project folder:
        ```powershell
        mkdir sales-pie-chart
        cd sales-pie-chart
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
        mkdir sales-pie-chart
        cd sales-pie-chart
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

## 3. Prepare the sales data file

Create a file named `sales_data.csv` in your project folder with the following content:

```csv
Region,Sales
Europe,120000
China,150000
```

## 4. Main code components

This section explains the main components of the code that uploads the sales data, creates an agent with the Code Interpreter tool, and generates a pie chart.

### Import required libraries

The code imports the Azure AI Projects client, identity, and code interpreter tool.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose
from azure.identity import DefaultAzureCredential
```

### Upload the sales data file

This code uploads the `sales_data.csv` file to your Azure AI Foundry project for use with the agent.

```python
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

file = project_client.agents.upload_file_and_poll(
    file_path="sales_data.csv",
    purpose=FilePurpose.AGENTS
)
print(f"Uploaded file, file ID: {file.id}")
```

### Create an agent with the Code Interpreter tool

This code creates an agent that can use the Code Interpreter tool and access the uploaded file.

```python
code_interpreter = CodeInterpreterTool(file_ids=[file.id])

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="sales-pie-chart-agent",
    instructions="You are a helpful assistant that generates charts from data.",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
print(f"Created agent, agent ID: {agent.id}")
```

### Create a thread and send a message to generate the pie chart

This code creates a conversation thread and sends a message instructing the agent to generate a pie chart.

```python
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Generate a sales by region pie chart using the sales_data.csv file."
)
print(f"Created message, message ID: {message.id}")
```

### Run the agent and retrieve the result

This code runs the agent and retrieves the result, including any generated files.

```python
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")

# Download any generated image files (pie chart)
for image_content in messages.image_contents:
    file_id = image_content.image_file.file_id
    file_name = f"{file_id}_pie_chart.png"
    project_client.agents.save_file(file_id=file_id, file_name=file_name)
    print(f"Saved pie chart image to: {file_name}")
```

## 5. Complete code example

The following is the complete code example. Save this as `example.py` in your project folder.

```python
"""
Generate a sales by region pie chart using the Code Interpreter tool in Azure AI Foundry Agents.
This script uploads a CSV file, creates an agent with the Code Interpreter, and generates a pie chart.
"""

import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose
from azure.identity import DefaultAzureCredential

def main():
    """
    Main function to upload sales data, create an agent, and generate a pie chart.
    """
    # Initialize the project client
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"]
    )

    with project_client:
        # Upload the sales data file
        file = project_client.agents.upload_file_and_poll(
            file_path="sales_data.csv",
            purpose=FilePurpose.AGENTS
        )
        print(f"Uploaded file, file ID: {file.id}")

        # Create the Code Interpreter tool
        code_interpreter = CodeInterpreterTool(file_ids=[file.id])

        # Create the agent
        agent = project_client.agents.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="sales-pie-chart-agent",
            instructions="You are a helpful assistant that generates charts from data.",
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
        )
        print(f"Created agent, agent ID: {agent.id}")

        # Create a thread
        thread = project_client.agents.create_thread()
        print(f"Created thread, thread ID: {thread.id}")

        # Send a message to generate the pie chart
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content="Generate a sales by region pie chart using the sales_data.csv file."
        )
        print(f"Created message, message ID: {message.id}")

        # Run the agent
        run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
        print(f"Run finished with status: {run.status}")

        if run.status == "failed":
            print(f"Run failed: {run.last_error}")

        # Retrieve and save the generated pie chart image
        messages = project_client.agents.list_messages(thread_id=thread.id)
        for image_content in messages.image_contents:
            file_id = image_content.image_file.file_id
            file_name = f"{file_id}_pie_chart.png"
            project_client.agents.save_file(file_id=file_id, file_name=file_name)
            print(f"Saved pie chart image to: {file_name}")

if __name__ == "__main__":
    main()
```

## 6. How to run the example code

1. Ensure you have created the `sales_data.csv` file as described above.
2. Set the required environment variables for your Azure AI Foundry project.
3. Run the script:

    ```bash
    python example.py
    ```

4. After the script completes, look for the generated pie chart image file in your project folder.

## Next steps

- Learn more about [Azure AI Foundry Agents](https://learn.microsoft.com/azure/ai-studio/concepts/agents-overview){:target="_blank"}
- Explore [Code Interpreter tool documentation](https://learn.microsoft.com/azure/ai-studio/concepts/agents-code-interpreter){:target="_blank"}
- Review [Azure AI Projects Python SDK reference](https://aka.ms/azsdk/azure-ai-projects/python/reference){:target="_blank"}
- Try adding more regions or sales data to your CSV file and rerun the script.