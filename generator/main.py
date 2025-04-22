"""Generates recipes using Azure OpenAI GPT-4.1 model."""

import os
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import yaml

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

ENDPOINT = "https://a4plaj2iwguui2-cog.openai.azure.com/openai/deployments/gpt-4.1"
MODEL_NAME = "gpt-4.1"

client = ChatCompletionsClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(API_KEY),
)


script_dir = Path(__file__).parent
parent_dir = script_dir.parent
system_message_file = parent_dir / "system_message.md"
with open(system_message_file, "r", encoding="utf-8") as f:
    system_message = f.read()

prompt_file_name = parent_dir / "prompts.yaml"

with open(prompt_file_name, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
if not isinstance(data, list):
    raise ValueError(
        "prompts.yaml must contain a top‑level list of prompt objects")


for idx, item in enumerate(data, start=1):
    name = item.get("name")
    filename = item.get("filename")
    prompt = item.get("prompt")

    response = client.complete(
        messages=[
            SystemMessage(content=system_message),
            UserMessage(content=prompt),
        ],
        temperature=0.1,
        top_p=0.1,
        model=MODEL_NAME,
    )

    print("Completed")

    recipe_file_name = parent_dir / "docs" / filename
    with open(recipe_file_name, "w", encoding="utf-8") as file:
        file.write(response.choices[0].message.content)
