# Generate a Sales by Region Pie Chart Using Azure AI Foundry Code Interpreter

This guide shows you how to use the Azure AI Foundry Code Interpreter tool to generate a pie chart of sales by region using sample data. You will upload a CSV file with sales data, create an agent with the Code Interpreter tool, and ask the agent to generate a pie chart.

## Prerequisites

- Python 3.8 or later
- Access to Azure AI Foundry services
- The following Python libraries:
  - `azure-ai-projects==1.0.0b9`
  - `azure-identity==1.21.0`

## 1. What You'll Learn

- How to set up your Python environment for Azure AI Foundry.
- How to upload a CSV file to Azure AI Foundry.
- How to create an agent with the Code Interpreter tool.
- How to generate a pie chart from sales data using the agent.

---

## 2. Environment Setup

### 2.1. Windows

1. **Create and activate a virtual environment:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install required libraries:**
   ```cmd
   pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0
   ```

3. **Set environment variables:**
   ```cmd
   set PROJECT_CONNECTION_STRING=<your-azure-ai-foundry-connection-string>
   set MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
   ```

### 2.2. Linux/macOS

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install required libraries:**
   ```bash
   pip install azure-ai-projects==1.0.0b9 azure-identity==1.21.0
   ```

3. **Set environment variables:**
   ```bash
   export PROJECT_CONNECTION_STRING=<your-azure-ai-foundry-connection-string>
   export MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
   ```

---

## 3. Prepare the Sales Data

Create a CSV file named `sales_by_region.csv` with the following content:

```csv
Region,Sales
Europe,120000
China,150000
```

---

## 4. Main Code Components

### 4.1. Import Libraries and Set Up Client

- Import required modules.
- Create an `AIProjectClient` using your Azure credentials and connection string.

### 4.2. Upload the CSV File

- Upload the `sales_by_region.csv` file to Azure AI Foundry for use with the Code Interpreter.

### 4.3. Create the Code Interpreter Tool

- Initialize the Code Interpreter tool with the uploaded file.

### 4.4. Create the Agent

- Create an agent with the Code Interpreter tool and provide instructions.

### 4.5. Create a Thread and Message

- Start a new thread and send a message asking the agent to generate a pie chart.

### 4.6. Run the Agent and Retrieve Results

- Run the agent and wait for completion.
- Download the generated pie chart image.

---

## 5. Complete Example Code

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose, MessageRole
from azure.identity import DefaultAzureCredential
from pathlib import Path

def main():
    # Set up the client
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"]
    )

    with project_client:
        # Upload the CSV file
        file = project_client.agents.upload_file_and_poll(
            file_path="sales_by_region.csv",
            purpose=FilePurpose.AGENTS
        )
        print(f"Uploaded file, file ID: {file.id}")

        # Set up the Code Interpreter tool with the uploaded file
        code_interpreter = CodeInterpreterTool(file_ids=[file.id])

        # Create the agent
        agent = project_client.agents.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="sales-assistant",
            instructions="You are a helpful assistant that generates charts from CSV data.",
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
            content="Generate a pie chart of sales by region from the uploaded CSV file."
        )
        print(f"Created message, message ID: {message.id}")

        # Run the agent
        run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
        print(f"Run finished with status: {run.status}")

        if run.status == "failed":
            print(f"Run failed: {run.last_error}")

        # Retrieve and save the generated image
        messages = project_client.agents.list_messages(thread_id=thread.id)
        for image_content in messages.image_contents:
            file_id = image_content.image_file.file_id
            file_name = f"{file_id}_sales_pie_chart.png"
            project_client.agents.save_file(file_id=file_id, file_name=file_name)
            print(f"Saved pie chart image to: {Path.cwd() / file_name}")

        # Clean up: delete agent and file
        project_client.agents.delete_agent(agent.id)
        print("Deleted agent")
        project_client.agents.delete_file(file.id)
        print("Deleted file")

if __name__ == "__main__":
    main()
```

---

## 6. How to Run the Example

1. Save the code above to a file, for example, `generate_sales_pie_chart.py`.
2. Ensure your `sales_by_region.csv` file is in the same directory.
3. Activate your virtual environment.
4. Set the required environment variables.
5. Run the script:

   ```bash
   python generate_sales_pie_chart.py
   ```

6. After completion, look for a PNG file in your directory. This is your sales by region pie chart.

---

## 7. Next Steps and Related Resources

- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-services/foundry/)
- [Azure AI Projects Python SDK reference](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme)
- [How to use the Code Interpreter tool](https://learn.microsoft.com/azure/ai-services/foundry/agents/code-interpreter)
- [Azure Identity authentication](https://learn.microsoft.com/azure/developer/python/sdk/identity)

---

**Tip:** You can modify the CSV file or the user message to generate different charts or analyze other data.