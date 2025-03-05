import time
from config import TAUTULLI_URL, TAUTULLI_API_KEY, USERNAME
from utils import fetch_data
from loguru import logger

def get_recently_watched():
    """Retrieve recently watched items from Tautulli."""
    one_hour_ago = int(time.time()) - 3600
    url = f"{TAUTULLI_URL}/api/v2?apikey={TAUTULLI_API_KEY}&cmd=get_history&length=20&user={USERNAME}&order_column=stopped"
    json_data = fetch_data(url)
    
    if not json_data:
        return []

    data = json_data.get("response", {}).get("data", {}).get("data", [])
    if not isinstance(data, list):
        logger.error(f"Unexpected response format: {type(data)} instead of list")
        return []

    return [item for item in data if item.get("stopped", 0) >= one_hour_ago]

def get_media_id(rating_key):
    """Get media GUIDs for mapping to Trakt."""
    url = f"{TAUTULLI_URL}/api/v2?apikey={TAUTULLI_API_KEY}&cmd=get_metadata&rating_key={rating_key}"
    metadata = fetch_data(url)
    if not metadata:
        return {}

    metadata = metadata.get("response", {}).get("data", {})
    if "guids" not in metadata:
        logger.warning(f"No GUIDs found for rating key {rating_key}")
        return {}

    for guid in metadata.get("guids", []):
        if "tmdb" in guid:
            return {"tmdb": int(guid.split("/")[-1])}
        elif "tvdb" in guid:
            return {"tvdb": int(guid.split("/")[-1])}
        elif "imdb" in guid:
            return {"imdb": guid.split("/")[-1]}
    
    return {}