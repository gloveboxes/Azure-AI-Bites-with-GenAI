# Generate a Sales by Region Pie Chart Using Azure AI Foundry Code Interpreter

This guide shows you how to use the Azure AI Foundry Code Interpreter tool to generate a pie chart of sales by region using sample data. You will upload a CSV file with sales data, create an agent with the Code Interpreter tool, and request a pie chart.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services
- An Azure AI Foundry project with a deployed model
- The following environment variables set:
  - `PROJECT_CONNECTION_STRING`
  - `MODEL_DEPLOYMENT_NAME`

## 1. Install Dependencies

1. Open a terminal or command prompt.
2. Create and activate a virtual environment:

   **Windows**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **Linux/macOS**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required Python packages:

   ```bash
   pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0
   ```

## 2. Prepare the Sales Data

1. Create a CSV file named `sales_by_region.csv` with the following content:

   ```csv
   Region,Sales
   Europe,120000
   China,150000
   ```

2. Save the file in your working directory.

## 3. Main Code Components Explained

The example code below performs these main steps:

- **Authenticate and connect** to your Azure AI Foundry project using `AIProjectClient` and `DefaultAzureCredential`.
- **Upload the CSV file** to Azure and wait for it to be processed.
- **Create a Code Interpreter tool** and associate it with the uploaded file.
- **Create an agent** with the Code Interpreter tool enabled.
- **Start a conversation thread** and send a user message requesting a pie chart.
- **Run the agent** to process the request.
- **Download and save the generated chart** from the agent's response.

## 4. Complete Code Example

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose, MessageRole
from azure.identity import DefaultAzureCredential
from pathlib import Path

# Set up the Azure AI Project client
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

    # Set up the Code Interpreter tool with the uploaded file
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

    # Create a conversation thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Send a user message requesting a pie chart
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Generate a sales by region pie chart using the uploaded CSV file."
    )
    print(f"Created message, message ID: {message.id}")

    # Run the agent to process the request
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Retrieve and save the generated chart image
    messages = project_client.agents.list_messages(thread_id=thread.id)
    for image_content in messages.image_contents:
        file_id = image_content.image_file.file_id
        file_name = f"{file_id}_sales_pie_chart.png"
        project_client.agents.save_file(file_id=file_id, file_name=file_name)
        print(f"Saved pie chart image to: {Path.cwd() / file_name}")

    # Clean up resources
    project_client.agents.delete_file(file.id)
    project_client.agents.delete_agent(agent.id)
    print("Cleaned up resources.")
```

## 5. How to Run the Example

1. Ensure your environment variables are set:

   ```bash
   # Example for Linux/macOS
   export PROJECT_CONNECTION_STRING="<your-connection-string>"
   export MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
   ```

2. Place `sales_by_region.csv` in your working directory.
3. Save the code above to a file, for example, `generate_sales_pie_chart.py`.
4. Run the script:

   ```bash
   python generate_sales_pie_chart.py
   ```

5. After completion, look for a PNG file in your directory (for example, `12345_sales_pie_chart.png`). This file contains the generated pie chart.

## 6. Next Steps and Related Resources

- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-services/foundry/)
- [Azure AI Projects Python SDK reference](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme)
- [How to use the Code Interpreter tool](https://learn.microsoft.com/azure/ai-services/foundry/agents/code-interpreter)
- [Azure Identity authentication](https://learn.microsoft.com/azure/developer/python/sdk/identity)

---

You have now generated a sales by region pie chart using the Azure AI Foundry Code Interpreter. For more advanced scenarios, explore additional tools and agent capabilities in Azure AI Foundry.