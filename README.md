# Azure AI Bites Generator

## Overview
The Azure AI Bites Generator is a tool designed to help you create bite-sized content for Azure AI. It generates a list of topics, each with a title, description, and a link to an external resource. The generated content is intended to be used for educational purposes, such as blog posts, social media updates, or internal training materials.

## Published Docs

The MkDocs for this project are published at [Azure AI Bites](https://gloveboxes.github.io/Azure-AI-Bites-with-GenAI/).

## Prerequisites
- Python 3.x
- OpenAI API key
- Deployed Azure AI Foundry GPT-4.1 Model

## Run the sample generator

```bash
cd generator
```

```bash
main.py
```

## Run the system message context generator

The system message context generator is a Python script that generates a system message context for the Azure AI Bites Generator. The script references the `system_message_context.yml` file which contains a list of titles and urls.

```bash
cd generator
```

```bash
python system_message_context.py
```
