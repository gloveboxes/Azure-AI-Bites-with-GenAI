# Generate a Sales by Region Pie Chart Using Code Interpreter

## Introduction

This guide shows you how to use the Code Interpreter tool in Azure AI Foundry Agents to generate a pie chart of sales by region from a CSV file. You will create a `sales_data.csv` file with sales data for Europe and China, and then use the Code Interpreter to visualize the data.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services

## 1. Authentication

Azure AI Foundry provides secure access to AI services and tools, including the Code Interpreter. You will need to authenticate using your Azure AI Foundry project connection string and model deployment name.

1. Go to the Azure AI Foundry portal.
2. Select your project and copy the **Project Connection String** from the **Overview** tab.
3. Find your model deployment name under the **Models + endpoints** tab.

## 2. Developer environment setup

Select your preferred operating system:

=== "Windows (PowerShell)"

    1. Open a terminal (PowerShell).
    2. Create a project folder:
        ```powershell
        mkdir code-interpreter-sales
        cd code-interpreter-sales
        ```
    3. Set up a virtual environment:
        ```powershell
        python -m venv .venv
        ```
    4. Activate the virtual environment:
        ```powershell
        .venv\Scripts\Activate
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
    2. Create a project folder:
        ```bash
        mkdir code-interpreter-sales
        cd code-interpreter-sales
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

## 3. Prepare the sales data CSV file

Create a file named `sales_data.csv` in your project folder with the following content:

```csv
Region,Sales
Europe,120000
China,150000
```

## 4. Main code components

### 4.1 Import required libraries

This section imports the necessary libraries for working with Azure AI Projects and authentication.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.ai.projects.models import FilePurpose
from azure.identity import DefaultAzureCredential
```

### 4.2 Upload the sales data file

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

### 4.3 Create an agent with the Code Interpreter tool

This code creates an agent that can use the Code Interpreter tool and access the uploaded file.

```python
from azure.ai.projects.models import CodeInterpreterTool

code_interpreter = CodeInterpreterTool(file_ids=[file.id])

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="sales-analyst",
    instructions="You are a helpful assistant that analyzes sales data.",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
print(f"Created agent, agent ID: {agent.id}")
```

### 4.4 Create a thread and request a pie chart

This code creates a conversation thread and sends a message to the agent, asking for a pie chart of sales by region.

```python
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Generate a pie chart of sales by region using the uploaded sales_data.csv file."
)
print(f"Created message, message ID: {message.id}")

run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")
```

### 4.5 Download and view the generated chart

This code retrieves the messages and downloads any generated image files (such as the pie chart).

```python
from pathlib import Path

messages = project_client.agents.list_messages(thread_id=thread.id)
for image_content in messages.image_contents:
    file_id = image_content.image_file.file_id
    file_name = f"{file_id}_sales_pie_chart.png"
    project_client.agents.save_file(file_id=file_id, file_name=file_name)
    print(f"Saved pie chart image to: {Path.cwd() / file_name}")
```

## 5. Complete code example

The following script combines all the steps above. Save this as `example.py` in your project folder.

```python
"""
Generate a sales by region pie chart using the Code Interpreter tool in Azure AI Foundry Agents.
This script uploads a CSV file, creates an agent with the Code Interpreter, and requests a pie chart.
"""

import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose
from azure.identity import DefaultAzureCredential

def main():
    # Authenticate and create the project client
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
            name="sales-analyst",
            instructions="You are a helpful assistant that analyzes sales data.",
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
        )
        print(f"Created agent, agent ID: {agent.id}")

        # Create a thread and send the analysis request
        thread = project_client.agents.create_thread()
        print(f"Created thread, thread ID: {thread.id}")

        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content="Generate a pie chart of sales by region using the uploaded sales_data.csv file."
        )
        print(f"Created message, message ID: {message.id}")

        run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
        print(f"Run finished with status: {run.status}")

        # Download the generated pie chart image
        messages = project_client.agents.list_messages(thread_id=thread.id)
        for image_content in messages.image_contents:
            file_id = image_content.image_file.file_id
            file_name = f"{file_id}_sales_pie_chart.png"
            project_client.agents.save_file(file_id=file_id, file_name=file_name)
            print(f"Saved pie chart image to: {Path.cwd() / file_name}")

if __name__ == "__main__":
    main()
```

This script uploads your sales data, creates an agent with the Code Interpreter, and requests a pie chart. The generated image will be saved in your project folder.

## 6. How to run the example code

1. Ensure you have created the `sales_data.csv` file as described above.
2. Set the required environment variables for your Azure AI Foundry project and model deployment.
3. Run the script:

    ```bash
    python example.py
    ```

4. After the script completes, look for the generated pie chart image in your project folder.

## Next steps

- Learn more about [Azure AI Foundry Agents](https://learn.microsoft.com/azure/ai-studio/concepts/agents-overview){:target="_blank"}
- Explore [Code Interpreter tool documentation](https://learn.microsoft.com/azure/ai-studio/concepts/agents-code-interpreter){:target="_blank"}
- Review [Azure AI Foundry model catalog](https://learn.microsoft.com/azure/ai-studio/how-to/model-catalog-overview){:target="_blank"}