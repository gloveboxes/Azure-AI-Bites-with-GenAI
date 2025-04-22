"""
This script fetches Python code from specified URLs writes them to a Markdown file.
These markdown file is appended to the system_message.md file to add context to the system message.
"""

from pathlib import Path

import requests
import yaml

# File paths
base_dir = Path(__file__).resolve().parent.parent
yaml_file = base_dir / "system_message_context.yml"
output_file = base_dir / "system_message_context.md"


# Load YAML
with open(yaml_file, "r", encoding="utf-8") as f:
    entries = yaml.safe_load(f)

# Clear or create output file
output_file.write_text("", encoding="utf-8")

# Fetch and append content
for entry in entries:
    title = entry["title"]
    url = entry["url"]

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        code = response.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        continue

    section = f"## {title.strip()}\n```python\n{code.strip()}\n```\n\n"

    with open(output_file, "a", encoding="utf-8") as f:
        f.write(section)

print(f"✅ All content written to {output_file}")
