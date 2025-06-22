
# APLMinT: Another Proxy LLM in Telegram

APLMinT is a versatile and robust Python-based Telegram bot that acts as a proxy to various Large Language Models (LLMs). It allows users to interact with multiple state-of-the-art AI models directly from their Telegram chat, with features designed for a seamless and controlled user experience.

**Usage:** The bot is accessible on Telegram at **[@aplmint_bot](https://t.me/aplmint_bot)**. Simply start a chat, select a model using the `/model` command, and start prompting!


*(Pro-tip: Take a screenshot of your bot in action and replace the URL above to make your README more engaging!)*

---

## ✨ Features

*   **Multi-Model Support:** Interact with a variety of powerful LLMs through the [OpenRouter API](https://openrouter.ai/).
*   **Interactive Model Selection:** Users can easily switch between models using a clean, interactive `/model` command with inline keyboard buttons.
*   **Intelligent Defaults:** The bot remembers the last model a user selected for subsequent queries, providing a smooth conversational flow.
*   **Rate Limiting:** A built-in daily query limit per user helps manage API usage and costs.
*   **Concurrency Control:** The bot intelligently handles simultaneous requests from a single user, preventing spam and ensuring orderly responses.
*   **Persistent Logging:** All query metadata (user, model used, timestamp) is logged to a lightweight SQLite database for analytics and monitoring.
*   **Dockerized for Deployment:** Comes with a `Dockerfile` for easy, consistent, and isolated deployment.
*   **Modern Development Environment:** Developed using `uv` for fast and efficient package management.

## 🛠️ Tech Stack

*   **Language:** Python 3.13
*   **Bot Framework:** [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (v22.1+)
*   **LLM Gateway:** [OpenRouter](https://openrouter.ai/)
*   **HTTP Client:** [httpx](https://www.python-httpx.org/) (asynchronous)
*   **Database:** SQLite
*   **Containerization:** Docker
*   **Package Manager:** [uv](https://github.com/astral-sh/uv)

## 🚀 Getting Started

To run this project locally, you will need Python 3.13+, `uv`, and Docker installed.

### 1. Clone the Repository

```bash
git clone https://github.com/heliomancer/aplmint.git
cd aplmint
```

### 2. Set Up the Development Environment

This project uses `uv` for managing the virtual environment and dependencies.

```bash
# Create the virtual environment
uv venv

# Activate the environment
source .venv/bin/activate

# Install the required packages
uv pip install -r requirements.txt
```

### 3. Configure Environment Variables

The bot requires API keys to function. These are managed through a `.env` file.

1.  Create a file named `.env` in the root of the project directory.
2.  Add your secret keys to this file. You will need:
    *   A **Telegram Bot Token** from [@BotFather](https://t.me/BotFather).
    *   An **OpenRouter API Key** from [openrouter.ai](https://openrouter.ai/keys).

```dotenv
# .env file content
TELEGRAM_BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
OPENROUTER_API_KEY="sk-or-your-long-open-router-api-key"
```

### 4. Run the Bot Locally

Ensure your virtual environment is activated and the `.env` file is configured.

Run the bot as a Python module from the project's root directory:

```bash
python -m src.bot
```

You should see log output indicating the database has been initialized and the bot is running. You can now interact with it on Telegram.

## 🐳 Deployment with Docker

The included `Dockerfile` allows you to build a self-contained image of the bot for easy deployment.

### 1. Build the Docker Image

From the project's root directory, run:

```bash
docker build -t aplmint .
```

### 2. Run the Docker Container

Run the image as a detached container, passing in the `.env` file to provide the necessary secrets.

```bash
docker run -d --name my-telegram-bot --env-file .env aplmint
```

**Useful Docker Commands:**
*   To view the logs of the running container: `docker logs my-telegram-bot`
*   To follow the logs in real-time: `docker logs -f my-telegram-bot`
*   To stop the container: `docker stop my-telegram-bot`
*   To remove the stopped container: `docker rm my-telegram-bot`

## 📂 Project Structure

The project follows a clean, modular structure within the `src/` directory.

```
aplmint/
├── src/
│   ├── __init__.py         # Makes 'src' a Python package
│   ├── bot.py              # Main entry point: initializes and runs the bot
│   ├── config.py           # Loads configuration and secrets
│   ├── database.py         # All SQLite database logic
│   ├── handlers.py         # All Telegram command and message handlers
│   └── llm_service.py      # Logic for communicating with the LLM API
├── .env.example            # Example environment file
├── .gitignore
├── Dockerfile
└── README.md
```

## 📝 Future Improvements

*   [ ] Implement conversation context/memory for each user.
*   [ ] Store conversation history in the SQLite database for persistence.
*   [ ] Add a token counting mechanism for more precise history management.
*   [ ] Introduce a system for user-defined system prompts.

---
*This project was created as part of a Python course.*