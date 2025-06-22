import httpx
import logging
from . import config

# Single instance of client
client = httpx.AsyncClient(timeout=30.0)

# log llm queries
logger = logging.getLogger(__name__)


async def get_llm_response(user_prompt: str, model_name: str) -> str:
    """Sends a prompt to the OpenRouter API using a specific model."""

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # OpenRouter uathentification policy standard
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/heliomancer/aplmint",
        "X-Title": "APLlMinT Bot", 
    }    
    
    payload = {
        "model": model_name, 
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Do not use markdown in your answers.source "},
            {"role": "user", "content": user_prompt}
        ],
    }

    logger.info(f"Sending prompt {user_prompt} to OpenRouter model {payload['model']}")
    try:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status() # This will raise an error for 4xx/5xx responses
        
        data = response.json()
        llm_text_response = data['choices'][0]['message']['content']
        return llm_text_response.strip()

    except httpx.HTTPStatusError as e:
        # This will give you more details if the API returns an error (e.g., bad key, invalid model)
        logger.error(f"OpenRouter API returned an error: {e}")
        logger.error(f"Response body: {e.response.text}")
        return "Sorry, there was an error communicating with the AI service. Please try again later."
    except httpx.RequestError as e:
        logger.error(f"A network error occurred: {e}")
        return "Sorry, I can't connect to the AI service right now. Please check the network."
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return "An unexpected error occurred while processing your request."