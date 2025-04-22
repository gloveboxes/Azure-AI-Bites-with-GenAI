## How to get a chat completions response from the service using a synchronous client and structured output
```python
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
DESCRIPTION:
    This sample demonstrates how to get a chat completions response from
    the service using a synchronous client and structured output. This sample
    directly defines a JSON schema for a cooking recipe, and it sets it as the desired
    `response_format` for a chat completions call asking how to bake a chocolate
    cake.

    Structured output is only supported by some Chat Completions models. This
    sample was run on a GPT-4o model hosted on Azure OpenAI, with api-version
    "2024-08-01-preview".

    If you are targeting a different endpoint (e.g. GitHub Models endpoint,
    Serverless API endpoint, Managed Compute endpoint) the client constructor may
    needs to be modified. See package documentation:
    https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/README.md#key-concepts

USAGE:
    python sample_chat_completions_with_structured_output.py

    Set these two environment variables before running the sample:
    1) AZURE_OPENAI_CHAT_ENDPOINT - Your AOAI endpoint URL, with partial path, in the form
        https://<your-unique-resouce-name>.openai.azure.com/openai/deployments/<your-deployment-name>
        where `your-unique-resource-name` is your globally unique AOAI resource name,
        and `your-deployment-name` is your AI Model deployment name.
        For example: https://your-unique-host.openai.azure.com/openai/deployments/gpt-4o
    2) AZURE_OPENAI_CHAT_KEY - Your model key. Keep it secret. This
        is only required for key authentication.

    Update `api_version` (the AOAI REST API version) as needed, based on the model documents.
    See also the "Data plane - inference" row in the table here for latest AOAI api-version:
    https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
"""


def sample_chat_completions_with_structured_output():
    import os
    import json

    from typing import Dict, Any
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import (
        SystemMessage,
        UserMessage,
        JsonSchemaFormat,
    )
    from azure.core.credentials import AzureKeyCredential

    try:
        endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
        key = os.environ["AZURE_OPENAI_CHAT_KEY"]
    except KeyError:
        print("Missing environment variable 'AZURE_OPENAI_CHAT_ENDPOINT' or 'AZURE_OPENAI_CHAT_KEY'")
        print("Set them before running this sample.")
        exit()

    # Defines a JSON schema for a cooking recipe. You would like the AI model to respond in this format.
    json_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The name of the recipe"},
            "servings": {"type": "integer", "description": "How many servings are in this recipe"},
            "ingredients": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the ingredient",
                        },
                        "quantity": {
                            "type": "string",
                            "description": "The quantity of the ingredient",
                        },
                    },
                    "required": ["name", "quantity"],
                    "additionalProperties": False,
                },
            },
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "step": {
                            "type": "integer",
                            "description": "Enumerates the step",
                        },
                        "directions": {
                            "type": "string",
                            "description": "Description of the recipe step",
                        },
                    },
                    "required": ["step", "directions"],
                    "additionalProperties": False,
                },
            },
            "prep_time": {
                "type": "integer",
                "description": "Preperation time in minutes",
            },
            "cooking_time": {
                "type": "integer",
                "description": "Cooking time in minutes",
            },
            "notes": {
                "type": "string",
                "description": "Any additional notes related to this recipe",
            },
        },
        "required": ["title", "servings", "ingredients", "steps", "prep_time", "cooking_time", "notes"],
        "additionalProperties": False,
    }

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="2024-08-01-preview",  # Azure OpenAI api-version. See https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
    )

    response = client.complete(
        response_format=JsonSchemaFormat(
            name="Recipe_JSON_Schema",
            schema=json_schema,
            description="Descripes a recipe in details, listing the ingredients, the steps and the time needed to prepare it",
            strict=True,
        ),
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("Please give me directions and ingredients to bake a chocolate cake."),
        ],
    )

    # Parse the JSON string response and print it in a nicely formatted way
    json_response_message = json.loads(response.choices[0].message.content)
    print(json.dumps(json_response_message, indent=4))


if __name__ == "__main__":
    sample_chat_completions_with_structured_output()
```

## how to use basic agent operations with function tools from the Azure Agents service
```python
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to use basic agent operations with function tools from
    the Azure Agents service using a synchronous client with tracing to console.

USAGE:
    python sample_agents_functions_with_console_tracing.py

    Before running the sample:

    pip install azure-ai-projects azure-identity opentelemetry-sdk azure-core-tracing-opentelemetry

    If you want to export telemetry to OTLP endpoint (such as Aspire dashboard
    https://learn.microsoft.com/dotnet/aspire/fundamentals/dashboard/standalone?tabs=bash)
    install:

    pip install opentelemetry-exporter-otlp-proto-grpc

    Set these environment variables with your own values:
    1) PROJECT_CONNECTION_STRING - The project connection string, as found in the overview page of your
       Azure AI Foundry project.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in 
       the "Models + endpoints" tab in your Azure AI Foundry project.
    3) AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED - Optional. Set to `true` to trace the content of chat
       messages, which may contain personal data. False by default.
"""
from typing import Any, Callable, Set

import os, sys, time, json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool, RequiredFunctionToolCall, SubmitToolOutputsAction, ToolOutput
from azure.ai.projects.telemetry import trace_function
from opentelemetry import trace

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

# Enable console tracing
# or, if you have local OTLP endpoint running, change it to
# project_client.telemetry.enable(destination="http://localhost:4317")
project_client.telemetry.enable(destination=sys.stdout)

scenario = os.path.basename(__file__)
tracer = trace.get_tracer(__name__)


# The trace_func decorator will trace the function call and enable adding additional attributes
# to the span in the function implementation. Note that this will trace the function parameters and their values.
@trace_function()
def fetch_weather(location: str) -> str:
    """
    Fetches the weather information for the specified location.

    :param location (str): The location to fetch weather for.
    :return: Weather information as a JSON string.
    :rtype: str
    """
    # In a real-world scenario, you'd integrate with a weather API.
    # Here, we'll mock the response.
    mock_weather_data = {"New York": "Sunny, 25°C", "London": "Cloudy, 18°C", "Tokyo": "Rainy, 22°C"}

    # Adding attributes to the current span
    span = trace.get_current_span()
    span.set_attribute("requested_location", location)

    weather = mock_weather_data.get(location, "Weather data not available for this location.")
    weather_json = json.dumps({"weather": weather})
    return weather_json


# Statically defined user functions for fast reference
user_functions: Set[Callable[..., Any]] = {
    fetch_weather,
}

# Initialize function tool with user function
functions = FunctionTool(functions=user_functions)

with tracer.start_as_current_span(scenario):
    with project_client:
        # Create an agent and run user's request with function calls
        agent = project_client.agents.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="my-assistant",
            instructions="You are a helpful assistant",
            tools=functions.definitions,
        )
        print(f"Created agent, ID: {agent.id}")

        thread = project_client.agents.create_thread()
        print(f"Created thread, ID: {thread.id}")

        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content="Hello, what is the weather in New York?",
        )
        print(f"Created message, ID: {message.id}")

        run = project_client.agents.create_run(thread_id=thread.id, agent_id=agent.id)
        print(f"Created run, ID: {run.id}")

        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)

            if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                if not tool_calls:
                    print("No tool calls provided - cancelling run")
                    project_client.agents.cancel_run(thread_id=thread.id, run_id=run.id)
                    break

                tool_outputs = []
                for tool_call in tool_calls:
                    if isinstance(tool_call, RequiredFunctionToolCall):
                        try:
                            output = functions.execute(tool_call)
                            tool_outputs.append(
                                ToolOutput(
                                    tool_call_id=tool_call.id,
                                    output=output,
                                )
                            )
                        except Exception as e:
                            print(f"Error executing tool_call {tool_call.id}: {e}")

                print(f"Tool outputs: {tool_outputs}")
                if tool_outputs:
                    project_client.agents.submit_tool_outputs_to_run(
                        thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                    )

            print(f"Current run status: {run.status}")

        print(f"Run completed with status: {run.status}")

        # Delete the agent when done
        project_client.agents.delete_agent(agent.id)
        print("Deleted agent")

        # Fetch and log all messages
        messages = project_client.agents.list_messages(thread_id=thread.id)
        print(f"Messages: {messages}")
```

## how to use agent operations with code interpreter from the Azure Agents service
```python
# pylint: disable=line-too-long,useless-suppression
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to use agent operations with code interpreter from
    the Azure Agents service using a synchronous client.

USAGE:
    python sample_agents_code_interpreter.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    1) PROJECT_CONNECTION_STRING - The project connection string, as found in the overview page of your
       Azure AI Foundry project.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in 
       the "Models + endpoints" tab in your Azure AI Foundry project.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.ai.projects.models import FilePurpose, MessageRole
from azure.identity import DefaultAzureCredential
from pathlib import Path

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:

    # Upload a file and wait for it to be processed
    # [START upload_file_and_create_agent_with_code_interpreter]
    file = project_client.agents.upload_file_and_poll(
        file_path="nifty_500_quarterly_results.csv", purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded file, file ID: {file.id}")

    code_interpreter = CodeInterpreterTool(file_ids=[file.id])

    # Create agent with code interpreter tool and tools_resources
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-assistant",
        instructions="You are helpful assistant",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    # [END upload_file_and_create_agent_with_code_interpreter]
    print(f"Created agent, agent ID: {agent.id}")

    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Create a message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Could you please create bar chart in TRANSPORTATION sector for the operating profit from the uploaded csv file and provide file to me?",
    )
    print(f"Created message, message ID: {message.id}")

    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    project_client.agents.delete_file(file.id)
    print("Deleted file")

    # [START get_messages_and_save_files]
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")

    for image_content in messages.image_contents:
        file_id = image_content.image_file.file_id
        print(f"Image File ID: {file_id}")
        file_name = f"{file_id}_image_file.png"
        project_client.agents.save_file(file_id=file_id, file_name=file_name)
        print(f"Saved image file to: {Path.cwd() / file_name}")

    for file_path_annotation in messages.file_path_annotations:
        print(f"File Paths:")
        print(f"Type: {file_path_annotation.type}")
        print(f"Text: {file_path_annotation.text}")
        print(f"File ID: {file_path_annotation.file_path.file_id}")
        print(f"Start Index: {file_path_annotation.start_index}")
        print(f"End Index: {file_path_annotation.end_index}")
    # [END get_messages_and_save_files]

    last_msg = messages.get_last_text_message_by_role(MessageRole.AGENT)
    if last_msg:
        print(f"Last Message: {last_msg.text.value}")

    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

## how to use agent operations with an event handler and toolset from the Azure Agents service
```python
# pylint: disable=line-too-long,useless-suppression
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to use agent operations with an event handler and toolset from
    the Azure Agents service using a synchronous client.

USAGE:
    python sample_agents_stream_eventhandler_with_functions_async.py

    Before running the sample:

    pip install azure-ai-projects azure-identity aiohttp

    Set this environment variables with your own values:
    PROJECT_CONNECTION_STRING - the Azure AI Project connection string, as found in your AI Foundry project.
"""
import asyncio
from typing import Any

import os
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import (
    AsyncAgentEventHandler,
    AsyncFunctionTool,
    MessageDeltaChunk,
    RequiredFunctionToolCall,
    RunStep,
    SubmitToolOutputsAction,
    ThreadMessage,
    ThreadRun,
    ToolOutput,
)
from azure.identity.aio import DefaultAzureCredential
from user_async_functions import user_async_functions


class MyEventHandler(AsyncAgentEventHandler[str]):

    def __init__(self, functions: AsyncFunctionTool, project_client: AIProjectClient) -> None:
        super().__init__()
        self.functions = functions
        self.project_client = project_client

    async def on_message_delta(self, delta: "MessageDeltaChunk") -> None:
        print(f"Text delta received: {delta.text}")

    async def on_thread_message(self, message: "ThreadMessage") -> None:
        print(f"ThreadMessage created. ID: {message.id}, Status: {message.status}")

    async def on_thread_run(self, run: "ThreadRun") -> None:
        print(f"ThreadRun status: {run.status}")

        if run.status == "failed":
            print(f"Run failed. Error: {run.last_error}")

        if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
            tool_calls = run.required_action.submit_tool_outputs.tool_calls

            tool_outputs = []
            for tool_call in tool_calls:
                if isinstance(tool_call, RequiredFunctionToolCall):
                    try:
                        output = await self.functions.execute(tool_call)
                        tool_outputs.append(
                            ToolOutput(
                                tool_call_id=tool_call.id,
                                output=output,
                            )
                        )
                    except Exception as e:
                        print(f"Error executing tool_call {tool_call.id}: {e}")

            print(f"Tool outputs: {tool_outputs}")
            if tool_outputs:
                await self.project_client.agents.submit_tool_outputs_to_stream(
                    thread_id=run.thread_id, run_id=run.id, tool_outputs=tool_outputs, event_handler=self
                )

    async def on_run_step(self, step: "RunStep") -> None:
        print(f"RunStep type: {step.type}, Status: {step.status}")

    async def on_error(self, data: str) -> None:
        print(f"An error occurred. Data: {data}")

    async def on_done(self) -> None:
        print("Stream completed.")

    async def on_unhandled_event(self, event_type: str, event_data: Any) -> None:
        print(f"Unhandled Event Type: {event_type}, Data: {event_data}")


async def main() -> None:
    async with DefaultAzureCredential() as creds:
        async with AIProjectClient.from_connection_string(
            credential=creds, conn_str=os.environ["PROJECT_CONNECTION_STRING"]
        ) as project_client:

            # [START create_agent_with_function_tool]
            functions = AsyncFunctionTool(functions=user_async_functions)

            agent = await project_client.agents.create_agent(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                name="my-assistant",
                instructions="You are a helpful assistant",
                tools=functions.definitions,
            )
            # [END create_agent_with_function_tool]
            print(f"Created agent, ID: {agent.id}")

            thread = await project_client.agents.create_thread()
            print(f"Created thread, thread ID {thread.id}")

            message = await project_client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content="Hello, send an email with the datetime and weather information in New York? Also let me know the details.",
            )
            print(f"Created message, message ID {message.id}")

            async with await project_client.agents.create_stream(
                thread_id=thread.id, agent_id=agent.id, event_handler=MyEventHandler(functions, project_client)
            ) as stream:
                await stream.until_done()

            await project_client.agents.delete_agent(agent.id)
            print("Deleted agent")

            messages = await project_client.agents.list_messages(thread_id=thread.id)
            print(f"Messages: {messages}")


if __name__ == "__main__":
    asyncio.run(main())
```

## how to add files to agent during the vector store creation
```python
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
DESCRIPTION:
    This sample demonstrates how to add files to agent during the vector store creation.

USAGE:
    python sample_agents_vector_store_file_search.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    1) PROJECT_CONNECTION_STRING - The project connection string, as found in the overview page of your
       Azure AI Foundry project.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in 
       the "Models + endpoints" tab in your Azure AI Foundry project.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, FilePurpose, MessageTextContent
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:

    # Upload a file and wait for it to be processed
    file = project_client.agents.upload_file_and_poll(file_path="product_info_1.md", purpose=FilePurpose.AGENTS)
    print(f"Uploaded file, file ID: {file.id}")

    # Create a vector store with no file and wait for it to be processed
    vector_store = project_client.agents.create_vector_store_and_poll(file_ids=[file.id], name="sample_vector_store")
    print(f"Created vector store, vector store ID: {vector_store.id}")

    # Create a file search tool
    file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])

    # Notices that FileSearchTool as tool and tool_resources must be added or the assistant unable to search the file
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-assistant",
        instructions="You are helpful assistant",
        tools=file_search_tool.definitions,
        tool_resources=file_search_tool.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")

    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    message = project_client.agents.create_message(
        thread_id=thread.id, role="user", content="What feature does Smart Eyewear offer?"
    )
    print(f"Created message, message ID: {message.id}")

    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Created run, run ID: {run.id}")

    project_client.agents.delete_vector_store(vector_store.id)
    print("Deleted vector store")

    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    messages = project_client.agents.list_messages(thread_id=thread.id)

    for message in reversed(messages.data):
        # To remove characters, which are not correctly handled by print, we will encode the message
        # and then decode it again.
        clean_message = "\n".join(
            text_msg.text.value.encode("ascii", "ignore").decode("utf-8") for text_msg in message.text_messages
        )
        print(f"Role: {message.role}  Message: {clean_message}")
```

## how to get a chat completions response from the service using a synchronous client, with an Azure OpenAI (AOAI) endpoint.
```python
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
DESCRIPTION:
    This sample demonstrates how to get a chat completions response from
    the service using a synchronous client, with an Azure OpenAI (AOAI) endpoint.
    Two types of authentications are shown: key authentication and Entra ID
    authentication.

USAGE:
    1. Update `key_auth` below to `True` for key authentication, or `False` for
       Entra ID authentication.
    2. Update `api_version` (the AOAI REST API version) as needed.
       See the "Data plane - inference" row in the table here for latest AOAI api-version:
       https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
    3. Set one or two environment variables, depending on your authentication method:
        * AZURE_OPENAI_CHAT_ENDPOINT - Your AOAI endpoint URL, with partial path, in the form
            https://<your-unique-resouce-name>.openai.azure.com/openai/deployments/<your-deployment-name>
            where `your-unique-resource-name` is your globally unique AOAI resource name,
            and `your-deployment-name` is your AI Model deployment name.
            For example: https://your-unique-host.openai.azure.com/openai/deployments/gpt-4o
        * AZURE_OPENAI_CHAT_KEY - Your model key. Keep it secret. This is only required for key authentication.
    4. Run the sample:
       python sample_chat_completions_azure_openai.py
"""


def sample_chat_completions_azure_openai():
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage

    try:
        endpoint = os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
    except KeyError:
        print("Missing environment variable 'AZURE_OPENAI_CHAT_ENDPOINT'")
        print("Set it before running this sample.")
        exit()

    key_auth = True  # Set to True for key authentication, or False for Entra ID authentication.

    if key_auth:
        from azure.core.credentials import AzureKeyCredential

        try:
            key = os.environ["AZURE_OPENAI_CHAT_KEY"]
        except KeyError:
            print("Missing environment variable 'AZURE_OPENAI_CHAT_KEY'")
            print("Set it before running this sample.")
            exit()

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key),
            api_version="2024-06-01",  # Azure OpenAI api-version. See https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
        )

    else:  # Entra ID authentication
        from azure.identity import DefaultAzureCredential

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
            credential_scopes=["https://cognitiveservices.azure.com/.default"],
            api_version="2024-06-01",  # Azure OpenAI api-version. See https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
        )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("How many feet are in a mile?"),
        ]
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    sample_chat_completions_azure_openai()
```

## Explore the model catalog in Azure AI Foundry portal
```markdown
---
title: Explore the model catalog in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces foundation model capabilities and the model catalog in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ai-learning-hub
  - ignite-2024
ms.topic: how-to
ms.date: 03/24/2025
ms.reviewer: jcioffi
ms.author: ssalgado
author: ssalgadodev
---

# Model catalog and collections in Azure AI Foundry portal

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

The model catalog in Azure AI Foundry portal is the hub to discover and use a wide range of models for building generative AI applications. The model catalog features hundreds of models across model providers such as Azure OpenAI Service, Mistral, Meta, Cohere, NVIDIA, and Hugging Face, including models that Microsoft trained. Models from providers other than Microsoft are Non-Microsoft Products as defined in [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage) and are subject to the terms provided with the models.

## Model collections

The model catalog organizes models into different collections:


* **Curated by Azure AI**: The most popular partner models (open-weight and proprietary) packaged and optimized to work seamlessly on the Azure AI platform. Use of these models is subject to the model providers' license terms. When you deploy these models in Azure AI Foundry portal, their availability is subject to the applicable [Azure service-level agreement (SLA)](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services), and Microsoft provides support for deployment problems.

  Models from partners such as Meta, NVIDIA, and Mistral AI are examples of models available in this collection on the catalog. You can identify these models by looking for a green checkmark on the model tiles in the catalog. Or you can filter by the **Curated by Azure AI** collection.

* **Azure OpenAI models exclusively available on Azure**: Flagship Azure OpenAI models available through an integration with Azure OpenAI Service. Microsoft supports these models and their use according to the product terms and [SLA for Azure OpenAI Service](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services).

* **Open models from the Hugging Face hub**: Hundreds of models from the Hugging Face hub for real-time inference with managed compute. Hugging Face creates and maintains models listed in this collection. For help, use the [Hugging Face forum](https://discuss.huggingface.co) or [Hugging Face support](https://huggingface.co/support). Learn more in [Deploy open models with Azure AI Foundry](deploy-models-managed.md).

You can submit a request to add a model to the model catalog by using [this form](https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbR_frVPkg_MhOoQxyrjmm7ZJUM09WNktBMURLSktOWEdDODBDRjg2NExKUy4u).

## Overview of model catalog capabilities

You can search and discover models that meet your need through `keyword search` and `filters`. Model catalog also offers the model performance benchmark metrics for select models. You can access the benchmark by clicking `Compare Models` or from the model card Benchmark tab.

On the model card, you'll find:

* **Quick facts**: you will see key information about the model at a quick glance.
* **Details**: this page contains the detailed information about the model, including description, version info, supported data type, etc.
* **Benchmarks**: you will find performance benchmark metrics for select models.
* **Existing deployments**: if you have already deployed the model, you can find it under Existing deployments tab.
* **Code samples**: you will find the basic code samples to get started with AI application development.
* **License**: you will find legal information related to model licensing.
* **Artifacts**: this tab will be displayed for open models only. You can see the model assets and download them via user interface.

## Model deployment: Azure OpenAI

For more information on Azure OpenAI models, see [What is Azure OpenAI Service?](../../ai-services/openai/overview.md).

## Model deployment: Managed compute and serverless APIs  

In addition to Azure OpenAI Service models, the model catalog offers two distinct ways to deploy models for your use: managed compute and serverless APIs.

The deployment options and features available for each model vary, as described in the following tables. [Learn more about data processing with the deployment options]( concept-data-privacy.md).

### Capabilities of model deployment options
<!-- docutune:disable -->

Features | Managed compute | Serverless API (pay-per-token)
--|--|--
Deployment experience and billing | Model weights are deployed to dedicated virtual machines with managed compute. A managed compute, which can have one or more deployments, makes available a REST API for inference. You're billed for the virtual machine core hours that the deployments use. | Access to models is through a deployment that provisions an API to access the model. The API provides access to the model that Microsoft hosts and manages, for inference. You're billed for inputs and outputs to the APIs, typically in tokens. Pricing information is provided before you deploy.
API authentication | Keys and Microsoft Entra authentication. | Keys only.
Content safety | Use Azure AI Content Safety service APIs. | Azure AI Content Safety filters are available integrated with inference APIs. Azure AI Content Safety filters are billed separately.
Network isolation | [Configure managed networks for Azure AI Foundry hubs](configure-managed-network.md).  | Managed compute follow your hub's public network access (PNA) flag setting. For more information, see the [Network isolation for models deployed via Serverless APIs](#network-isolation-for-models-deployed-via-serverless-apis) section later in this article.

### Available models for supported deployment options

For Azure OpenAI models, see [Azure OpenAI Service Models](../../ai-services/openai/concepts/models.md).

To view a list of supported models for Serverless API or Managed Compute, go to the home page of the model catalog in [Azure AI Foundry](https://ai.azure.com). Use the **Deployment options** filter to select either **Serverless API** or **Managed Compute**. 

:::image type="content" source="../media/how-to/model-catalog-overview/catalog-filter.png" alt-text="A screenshot showing how to filter by managed compute models in the catalog." lightbox="../media/how-to/model-catalog-overview/catalog-filter.png":::  


<!-- docutune:enable -->

:::image type="content" source="../media/explore/platform-service-cycle.png" alt-text="Diagram that shows models as a service and the service cycle of managed computes." lightbox="../media/explore/platform-service-cycle.png":::

## Model lifecycle: deprecation and retirement
AI models evolve fast, and when a new version or a new model with updated capabilities in the same model family become available, older models may be retired in the AI Foundry model catalog. To allow for a smooth transition to a newer model version, some models provide users with the option to enable automatic updates. To learn more about the model lifecycle of different models, upcoming model retirement dates, and suggested replacement models and versions, see:

- [Azure OpenAI Service model deprecations and retirements](../../ai-services/openai/concepts/model-retirements.md)
- [Serverless API model deprecations and retirements](../concepts/model-lifecycle-retirement.md)

## Managed compute

The capability to deploy models as managed compute builds on platform capabilities of Azure Machine Learning to enable seamless integration of the wide collection of models in the model catalog across the entire life cycle of large language model (LLM) operations.

:::image type="content" source="../media/explore/llmops-life-cycle.png" alt-text="Diagram that shows the life cycle of large language model operations." lightbox="../media/explore/llmops-life-cycle.png":::

### Availability of models for deployment as managed compute  

The models are made available through [Azure Machine Learning registries](/azure/machine-learning/concept-machine-learning-registries-mlops). These registries enable a machine-learning-first approach to [hosting and distributing Azure Machine Learning assets](/azure/machine-learning/how-to-share-models-pipelines-across-workspaces-with-registries). These assets include model weights, container runtimes for running the models, pipelines for evaluating and fine-tuning the models, and datasets for benchmarks and samples.

The registries build on top of a highly scalable and enterprise-ready infrastructure that:

* Delivers low-latency access model artifacts to all Azure regions with built-in geo-replication.

* Supports enterprise security requirements such as limiting access to models by using Azure Policy and secure deployment by using managed virtual networks.

### Deployment of models for inference with managed compute

Models available for deployment to managed compute can be deployed to Azure Machine Learning managed compute for real-time inference. Deploying to managed compute requires you to have a virtual machine quota in your Azure subscription for the specific products that you need to optimally run the model. Some models allow you to deploy to a [temporarily shared quota for model testing](deploy-models-managed.md).

Learn more about deploying models:

* [Deploy Meta Llama models](deploy-models-llama.md)
* [Deploy Azure AI Foundry open models](deploy-models-managed.md)

### Building generative AI apps with managed compute

The *prompt flow* feature in Azure Machine Learning offers a great experience for prototyping. You can use models deployed with managed compute in prompt flow with the [Open Model LLM tool](/azure/machine-learning/prompt-flow/tools-reference/open-model-llm-tool). You can also use the REST API exposed by managed compute in popular LLM tools like LangChain with the [Azure Machine Learning extension](https://python.langchain.com/docs/integrations/chat/azureml_chat_endpoint/).  

### Content safety for models deployed as managed compute

The [Azure AI Content Safety](../../ai-services/content-safety/overview.md) service is available for use with managed compute to screen for various categories of harmful content, such as sexual content, violence, hate, and self-harm. You can also use the service to screen for advanced threats such as jailbreak risk detection and protected material text detection.

You can refer to [this notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/system/inference/text-generation/llama-safe-online-deployment.ipynb) for reference integration with Azure AI Content Safety for Llama 2. Or you can use the Content Safety (Text) tool in prompt flow to pass responses from the model to Azure AI Content Safety for screening. You're billed separately for such use, as described in [Azure AI Content Safety pricing](https://azure.microsoft.com/pricing/details/cognitive-services/content-safety/).

## Serverless API (pay-per-token) billing

You can deploy certain models in the model catalog with pay-per-token billing. This deployment method, also called *Serverless API*, provides a way to consume the models as APIs without hosting them on your subscription. Models are hosted in a Microsoft-managed infrastructure, which enables API-based access to the model provider's model. API-based access can dramatically reduce the cost of accessing a model and simplify the provisioning experience.

Models that are available for deployment as serverless APIs with pay-as-you-go billing are offered by the model provider, but they're hosted in a Microsoft-managed Azure infrastructure and accessed via API. Model providers define the license terms and set the price for use of their models. The Azure Machine Learning service:

* Manages the hosting infrastructure.
* Makes the inference APIs available.
* Acts as the data processor for prompts submitted and content output by models deployed via MaaS.

Learn more about data processing for MaaS in the [article about data privacy](concept-data-privacy.md).

:::image type="content" source="../media/explore/model-publisher-cycle.png" alt-text="Diagram that shows the model publisher service cycle." lightbox="../media/explore/model-publisher-cycle.png":::

> [!NOTE]
> Cloud Solution Provider (CSP) subscriptions do not have the ability to purchase serverless API deployments (MaaS) models.

### Billing

The discovery, subscription, and consumption experience for models deployed via MaaS is in Azure AI Foundry portal and Azure Machine Learning studio. Users accept license terms for use of the models. Pricing information for consumption is provided during deployment.

Models from non-Microsoft providers are billed through Azure Marketplace, in accordance with the [Microsoft Commercial Marketplace Terms of Use](/legal/marketplace/marketplace-terms).

Models from Microsoft are billed via Azure meters as First Party Consumption Services. As described in the [Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), you purchase First Party Consumption Services by using Azure meters, but they aren't subject to Azure service terms. Use of these models is subject to the provided license terms.  

### Fine-tuning models

Certain models also support fine-tuning. For these models, you can take advantage of managed compute (preview) or serverless API fine-tuning to tailor the models by using data that you provide. For more information, see the [fine-tuning overview](../concepts/fine-tuning-overview.md).

### RAG with models deployed as serverless APIs

In Azure AI Foundry portal, you can use vector indexes and retrieval-augmented generation (RAG). You can use models that can be deployed via serverless APIs to generate embeddings and inferencing based on custom data. These embeddings and inferencing can then generate answers specific to your use case. For more information, see [Build and consume vector indexes in Azure AI Foundry portal](index-add.md).

### Regional availability of offers and models

Pay-per-token billing is available only to users whose Azure subscription belongs to a billing account in a country/region where the model provider has made the offer available. If the offer is available in the relevant region, the user then must have a project resource in the Azure region where the model is available for deployment or fine-tuning, as applicable. See [Region availability for models in serverless API endpoints | Azure AI Foundry](deploy-models-serverless-availability.md) for detailed information.

### Content safety for models deployed via serverless APIs

[!INCLUDE [content-safety-serverless-models](../includes/content-safety-serverless-models.md)]

### Network isolation for models deployed via serverless APIs

Endpoints for models deployed as serverless APIs follow the public network access flag setting of the Azure AI Foundry hub that has the project in which the deployment exists. To help secure your serverless API endpoint, disable the public network access flag on your Azure AI Foundry hub. You can help secure inbound communication from a client to your endpoint by using a private endpoint for the hub.

To set the public network access flag for the Azure AI Foundry hub:

* Go to the [Azure portal](https://ms.portal.azure.com/).
* Search for the resource group to which the hub belongs, and select your Azure AI Foundry hub from the resources listed for this resource group.
* On the hub overview page, on the left pane, go to **Settings** > **Networking**.
* On the **Public access** tab, you can configure settings for the public network access flag.
* Save your changes. Your changes might take up to five minutes to propagate.

#### Limitations

* If you have an Azure AI Foundry hub with a private endpoint created before July 11, 2024, serverless API endpoints added to projects in this hub won't follow the networking configuration of the hub. Instead, you need to create a new private endpoint for the hub and create new serverless API deployments in the project so that the new deployments can follow the hub's networking configuration.

* If you have an Azure AI Foundry hub with MaaS deployments created before July 11, 2024, and you enable a private endpoint on this hub, the existing serverless API deployments won't follow the hub's networking configuration. For serverless API deployments in the hub to follow the hub's networking configuration, you need to create the deployments again.

* Currently, [Azure OpenAI On Your Data](/azure/ai-services/openai/concepts/use-your-data) support isn't available for serverless API deployments in private hubs, because private hubs have the public network access flag disabled.

* Any network configuration change (for example, enabling or disabling the public network access flag) might take up to five minutes to propagate.

## Related content

* [Explore foundation models in Azure AI Foundry portal](../../ai-services/connect-services-ai-foundry-portal.md)
* [Model deprecation and retirement in Azure AI model catalog](../concepts/model-lifecycle-retirement.md)
```

