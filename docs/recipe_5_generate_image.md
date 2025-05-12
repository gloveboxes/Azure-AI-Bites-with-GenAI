# Generate a Sales by Region Pie Chart Using Code Interpreter in Azure AI Foundry

## Introduction

This article demonstrates how to use the Code Interpreter tool in Azure AI Foundry Agents to generate a pie chart of sales by region from a CSV file. You will use a project connection string and Microsoft Entra ID authentication to securely access the Azure AI Foundry project and run the code interpreter tool.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Authentication

This example uses a project connection string and Microsoft Entra ID authentication.

The **project connection string** is a unique string that allows your application to connect to your Azure AI Foundry project. You can find it in the **Overview** tab of your Azure AI Foundry project in the Azure portal, under **Project details**.

**Microsoft Entra ID authentication** uses your Azure identity to securely access Azure resources. You can authenticate using your Azure account credentials. To use this method, ensure you have the necessary permissions and have signed in using the Azure CLI (`az login`).

**Steps:**

1. Go to the Azure portal and navigate to your Azure AI Foundry project.
2. Copy the **Project Connection String** from the **Overview** tab.
3. Ensure you have the Azure CLI installed and run `az login` to authenticate with Microsoft Entra ID.

## 2. Developer environment setup

Select your preferred operating system:

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a project folder:
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
        $env:PROJECT_CONNECTION_STRING = "<your-project-connection-string>"
        $env:MODEL_DEPLOYMENT_NAME = "<your-model-deployment-name>"
        ```

=== "Linux/macOS"

    1. Open a terminal.
    2. Create a project folder:
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

## 4. Code Sample

This code sample demonstrates how to use the Code Interpreter tool in Azure AI Foundry Agents to generate a pie chart from the sales data.

### Main code components

#### Import required libraries

This section imports the necessary Python libraries for authentication and interaction with Azure AI Foundry.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose
from azure.identity import DefaultAzureCredential
from pathlib import Path
```

#### Upload the sales data file

This code uploads the `sales_data.csv` file to your Azure AI Foundry project for use with the Code Interpreter.

```python
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    file = project_client.agents.upload_file_and_poll(
        file_path="sales_data.csv",
        purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded file, file ID: {file.id}")
```

#### Create an agent with the Code Interpreter tool

This code creates an agent with the Code Interpreter tool, referencing the uploaded file.

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

#### Create a thread and message to request the pie chart

This code creates a thread and sends a message to the agent, instructing it to generate a pie chart.

```python
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Generate a pie chart of sales by region using the sales_data.csv file."
    )
    print(f"Created message, message ID: {message.id}")
```

#### Run the agent and save the generated chart

This code runs the agent, retrieves the generated chart, and saves it locally.

```python
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    messages = project_client.agents.list_messages(thread_id=thread.id)
    for image_content in messages.image_contents:
        file_id = image_content.image_file.file_id
        file_name = f"{file_id}_sales_pie_chart.png"
        project_client.agents.save_file(file_id=file_id, file_name=file_name)
        print(f"Saved pie chart image to: {Path.cwd() / file_name}")

    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
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
from pathlib import Path

def main():
    """
    Main function to upload sales data, create an agent with the Code Interpreter tool,
    and generate a pie chart of sales by region.
    """
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

        # Create a thread and message
        thread = project_client.agents.create_thread()
        print(f"Created thread, thread ID: {thread.id}")

        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content="Generate a pie chart of sales by region using the sales_data.csv file."
        )
        print(f"Created message, message ID: {message.id}")

        # Run the agent
        run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
        print(f"Run finished with status: {run.status}")

        # Retrieve and save the generated chart
        messages = project_client.agents.list_messages(thread_id=thread.id)
        for image_content in messages.image_contents:
            file_id = image_content.image_file.file_id
            file_name = f"{file_id}_sales_pie_chart.png"
            project_client.agents.save_file(file_id=file_id, file_name=file_name)
            print(f"Saved pie chart image to: {Path.cwd() / file_name}")

        # Clean up
        project_client.agents.delete_agent(agent.id)
        print("Deleted agent")

if __name__ == "__main__":
    main()
```

## 6. How to run the example code

1. Ensure you have created the `sales_data.csv` file in your project folder.
2. Set the required environment variables as described in the developer environment setup.
3. Run the script:

    ```bash
    python example.py
    ```

4. After the script completes, the generated pie chart image will be saved in your project folder.

## Next steps

- Learn more about [Azure AI Foundry Agents](https://learn.microsoft.com/azure/ai-studio/concepts/agents-overview){:target="_blank"}
- Explore [Code Interpreter tool documentation](https://learn.microsoft.com/azure/ai-studio/concepts/agents-code-interpreter){:target="_blank"}
- Review [Azure AI Foundry authentication options](https://learn.microsoft.com/azure/ai-studio/concepts/authentication){:target="_blank"}
- See more [Azure AI Foundry code samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples){:target="_blank"}
