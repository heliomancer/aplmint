import httpx
from . import config

# It's good practice to create a single client instance to be reused
client = httpx.AsyncClient(timeout=30.0)

async def get_llm_response(user_prompt: str) -> str:
    """
    Sends a prompt to the OpenRouter API using the async 'httpx' library.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # OpenRouter uses a standard Bearer token for authentication.
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/heliomancer/aplmint",
        "X-Title": "APLlMinT Bot", 
    }
    
    # This is the most important part: specifying a free model.
    # Go to https://openrouter.ai/models to see the full list of free models.
    # Examples:
    # - "mistralai/mistral-7b-instruct:free"
    # - "google/gemma-7b-it:free"
    # - "nousresearch/nous-hermes-2-mixtral-8x7b-dpo:free"
    # We'll use Mistral 7B as it's a great, fast, general-purpose model.
    
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt}
        ],
    }

    print(f"Sending prompt to OpenRouter with model {payload['model']}: '{user_prompt}'")
    try:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status() # This will raise an error for 4xx/5xx responses
        
        data = response.json()
        llm_text_response = data['choices'][0]['message']['content']
        return llm_text_response.strip()

    except httpx.HTTPStatusError as e:
        # This will give you more details if the API returns an error (e.g., bad key, invalid model)
        print(f"OpenRouter API returned an error: {e}")
        print(f"Response body: {e.response.text}")
        return "Sorry, there was an error communicating with the AI service. Please check the logs."
    except httpx.RequestError as e:
        print(f"A network error occurred: {e}")
        return "Sorry, I can't connect to the AI service right now. Please check the network."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred while processing your request."