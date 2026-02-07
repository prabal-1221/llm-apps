# 🌟 Featured AI Projects

Welcome to a curated collection of AI agents and applications. This repository serves as a hub for exploring various agentic frameworks, showcasing how large language models can be orchestrated to perform complex tasks.

## 📂 Table of Contents
- [🤖 AI Agents](#-ai-agents)
- [🛠️ Getting Started](#️-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)

---

## 🤖 AI Agents

Here you will find a growing list of intelligent agents, categorized by their complexity and use case.

### 🌱 Starter AI Agents
These projects are perfect for understanding the fundamentals of building agents with tools like LangGraph and Gemini.

* ### [🎙️ **AI Blog to Podcast Agent**](./blog_to_podcast_ai_agent)
    A smart agent that takes any blog post URL, summarizes it into a two-person dialogue script, and generates a realistic podcast audio file using text-to-speech.
    * **Tech Stack:** LangGraph, Google Gemini, Edge TTS, Trafilatura.
    * **Key Concepts:** State management, tool use, structured output, audio generation.

*(More agents will be added here soon...)*

---

## 🛠️ Getting Started

Follow these general steps to set up and run any of the projects in this repository.

### Prerequisites

* **Python 3.10+**
* **[uv](https://github.com/astral-sh/uv)**: A fast, modern Python package manager. We use it for managing dependencies and virtual environments.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/prabal-1221/llm-apps.git
    cd agent-folder
    ```

2.  **Sync dependencies:**
    Use `uv` to create a virtual environment and install all required packages locked in `uv.lock`.
    ```bash
    uv sync
    ```

### Environment Setup

Most AI agents require API keys to access LLMs (like Gemini, OpenAI, etc.).

1.  Create a `.env` file in the root directory of the repository.
2.  Add the necessary API keys. For example, for the **Blog to Podcast Agent**:
    ```env
    # .env file
    GOOGLE_API_KEY=your_actual_gemini_api_key_here
    ```

### Running a Project

You can use `uv run` to execute a script within the project's virtual environment easily.