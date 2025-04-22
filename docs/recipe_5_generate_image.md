# Generate a Sales by Region Pie Chart Using Azure AI Foundry Code Interpreter

This guide shows you how to use the Azure AI Foundry Code Interpreter tool to generate a pie chart of sales by region using sample data. You will upload a CSV file with sales data, create an agent with the Code Interpreter tool, and request a pie chart visualization.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services
- The following Python libraries:
  - `azure-ai-projects==1.0.0b9`
  - `azure-identity==1.21.0`

## 1. Introduction

You will create a CSV file with sales data by region, upload it to Azure AI Foundry, and use an agent with the Code Interpreter tool to generate a pie chart. The agent will process your request and return the chart as an image file.

---

## 2. Environment Setup

### 2.1. Windows

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

### 2.2. Linux/macOS

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

---

## 3. Main Code Components

### 3.1. Prepare the Sales Data

Create a CSV file named `sales_by_region.csv` with the following content:

```csv
Region,Sales
Europe,120000
China,150000
```

### 3.2. Upload the File and Create the Agent

- Upload the CSV file to Azure AI Foundry.
- Create an agent with the Code Interpreter tool, referencing the uploaded file.

### 3.3. Request the Pie Chart

- Send a message to the agent asking for a pie chart of sales by region.
- Retrieve and save the generated image file.

---

## 4. Complete Example Code

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose, MessageRole
from azure.identity import DefaultAzureCredential
from pathlib import Path

# Ensure the CSV file exists
csv_filename = "sales_by_region.csv"
if not os.path.exists(csv_filename):
    with open(csv_filename, "w") as f:
        f.write("Region,Sales\nEurope,120000\nChina,150000\n")

# Initialize the client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    # Upload the CSV file
    file = project_client.agents.upload_file_and_poll(
        file_path=csv_filename, purpose=FilePurpose.AGENTS
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

    # Send the request to generate a pie chart
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Generate a sales by region pie chart using the uploaded CSV file.",
    )
    print(f"Created message, message ID: {message.id}")

    # Run the agent
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    # Retrieve and save the image file
    messages = project_client.agents.list_messages(thread_id=thread.id)
    for image_content in messages.image_contents:
        file_id = image_content.image_file.file_id
        file_name = f"{file_id}_sales_by_region_pie_chart.png"
        project_client.agents.save_file(file_id=file_id, file_name=file_name)
        print(f"Saved pie chart image to: {Path.cwd() / file_name}")

    # Clean up resources
    project_client.agents.delete_file(file.id)
    project_client.agents.delete_agent(agent.id)
    print("Cleaned up resources.")
```

---

## 5. How to Run the Example

1. Save the code above to a file, for example, `generate_sales_pie_chart.py`.
2. Ensure your environment variables are set as described in the setup section.
3. Run the script:
   ```bash
   python generate_sales_pie_chart.py
   ```
4. After completion, look for a PNG file in your working directory. This file is the generated pie chart.

---

## 6. Next Steps

- Explore [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/){:target="_blank"} for more advanced agent and tool usage.
- Try uploading different datasets and requesting other types of visualizations.
- Review the [Azure AI Projects Python SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects){:target="_blank"} for more features.

---

**Related resources:**
- [Azure AI Foundry Quickstart](https://learn.microsoft.com/azure/ai-foundry/quickstart){:target="_blank"}
- [Azure AI Projects SDK Reference](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme){:target="_blank"}