import os

# Free models from openrouter
models = {'DeepSeek': 'deepseek/deepseek-chat:free',
          'Gemini': 'google/gemini-2.0-flash-exp:free',
          'Devstral': 'mistralai/devstral-small:free',
          'Mistral 7b': 'mistralai/mistral-7b-instruct:free',
          'Gemma 7b': 'google/gemma-7b-it:free'
          }


# Here secret keys taken from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("Access tokens are not set!")