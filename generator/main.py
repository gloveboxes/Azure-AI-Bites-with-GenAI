#!/usr/bin/env python3
"""
Generates recipes using Azure OpenAI GPT-4.1 model and updates MkDocs navigation.
"""

import os
from pathlib import Path
import yaml
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential


MODEL_NAME = "gpt-4.1"
TEMPERATURE = 0.1
TOP_P = 0.1
MAX_TOKENS = 30000


def load_environment(env_path: Path = None) -> None:
    """Load environment variables from .env file."""
    load_dotenv(dotenv_path=env_path)


def get_api_client(api_key: str, endpoint: str) -> ChatCompletionsClient:
    """Initialize and return ChatCompletionsClient."""
    return ChatCompletionsClient(
        endpoint=endpoint, credential=AzureKeyCredential(api_key)
    )


def load_and_combine_system_messages(base_path: Path, context_path: Path) -> str:
    """Read and return the system message content with context appended."""
    with open(base_path, encoding="utf-8") as f1, open(
        context_path, encoding="utf-8"
    ) as f2:
        base_content = f1.read()
        context_content = f2.read()
        return f"{base_content.strip()}\n\n{context_content.strip()}"


def load_yaml(path: Path):
    """Load and return YAML data."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_recipe(
    client: ChatCompletionsClient,
    system_message: str,
    prompt: str,
    model_name: str,
    **kwargs,
) -> str:
    """Generate a recipe using Azure OpenAI and return its content."""
    response = client.complete(
        messages=[SystemMessage(content=system_message), UserMessage(content=prompt)],
        model=model_name,
        **kwargs,
    )
    print(f"Response usage: {response.usage.total_tokens} tokens")
    return response.choices[0].message.content


def write_text(path: Path, text: str) -> None:
    """Ensure directory exists and write text to the given file path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def process_recipes(
    client: ChatCompletionsClient,
    data: list,
    docs_dir: Path,
    system_message: str,
    model_name: str,
) -> list:
    """Generate recipe files and return metadata for navigation."""
    recipes = []
    for item in data:
        title = item.get("title")
        filename = item.get("filename")
        prompt = item.get("prompt")
        target_path = docs_dir / filename

        recipes.append({"title": title, "filename": filename})

        if target_path.exists():
            print(f"Skipping {title}: {filename} already exists.")
            continue

        print(f"Generating {title}...")
        content = generate_recipe(
            client,
            system_message,
            prompt,
            model_name,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=MAX_TOKENS,
        )
        write_text(target_path, content)
        print(f"Completed {title}")

    return recipes


def update_mkdocs_nav(nav_items: list, mkdocs_path: Path) -> None:
    """Update the nav section in mkdocs.yml with the given items."""
    mkdocs_data = load_yaml(mkdocs_path)
    if not isinstance(mkdocs_data, dict):
        raise ValueError(
            "mkdocs.yml must contain a top-level dictionary of configuration options"
        )

    mkdocs_data["nav"] = [{item["title"]: item["filename"]} for item in nav_items]
    write_text(mkdocs_path, yaml.dump(mkdocs_data, sort_keys=False))


def main():
    """Main function to load environment, generate recipes, and update MkDocs."""
    base_dir = Path(__file__).resolve().parent.parent
    load_environment(base_dir / ".env")

    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_API_ENDPOINT")

    client = get_api_client(api_key, endpoint)
    system_message = load_and_combine_system_messages(
        base_dir / "system_message.md", base_dir / "system_message_context.md"
    )

    recipes_data = load_yaml(base_dir / "recipes.yml")
    if not isinstance(recipes_data, list):
        raise ValueError("recipes.yml must contain a top-level list of prompt objects")

    docs_dir = base_dir / "docs"
    recipes = process_recipes(
        client, recipes_data, docs_dir, system_message, MODEL_NAME
    )

    update_mkdocs_nav(recipes, base_dir / "mkdocs.yml")
    print(f"✅ Injected {len(recipes)} recipes into nav section of mkdocs.yml")


if __name__ == "__main__":
    main()
