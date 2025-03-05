import requests
import json
from loguru import logger

def fetch_data(url):
    """Make a GET request and return the JSON response."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON: {e}")
        return None