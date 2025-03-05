import time
import json
from datetime import datetime, timezone
import requests
from requests_oauthlib import OAuth2Session
from config import TRAKT_CLIENT_ID, TRAKT_CLIENT_SECRET, TRAKT_REDIRECT_URI, TOKEN_FILE
from tautulli import get_media_id
from loguru import logger

trakt = OAuth2Session(TRAKT_CLIENT_ID, redirect_uri=TRAKT_REDIRECT_URI)

def get_trakt_token():
    """Retrieve or request a new Trakt token."""
    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        auth_url, _ = trakt.authorization_url("https://trakt.tv/oauth/authorize")
        print(f"Go to this URL to authorize: {auth_url}")
        auth_code = input("Enter the code from Trakt: ")
        token = trakt.fetch_token("https://trakt.tv/oauth/token",
                                  client_secret=TRAKT_CLIENT_SECRET,
                                  code=auth_code)
        with open(TOKEN_FILE, "w") as f:
            json.dump(token, f)
        return token

trakt.token = get_trakt_token()

def refresh_trakt_token():
    """Refresh Trakt token if expired."""
    token = trakt.token
    if token["expires_at"] - 300 < time.time():
        logger.info("Refreshing Trakt token...")
        new_token = trakt.fetch_token("https://trakt.tv/oauth/token",
                                      client_id=TRAKT_CLIENT_ID,
                                      client_secret=TRAKT_CLIENT_SECRET,
                                      refresh_token=token["refresh_token"])
        with open(TOKEN_FILE, "w") as f:
            json.dump(new_token, f)
        trakt.token = new_token

def log_success(item):
    """Log successful sync to Trakt."""
    media_type = item.get("media_type")
    full_title = item.get("full_title")
    episode_no = item.get("media_index")
    season_no = item.get("parent_media_index")
    year = item.get("year")
    watched_at = datetime.fromtimestamp(item["date"], timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    if media_type == "episode":
        logger.info(f"Marked *{full_title} (S{season_no:02}E{episode_no:02})* as watched on Trakt.")
    else:
        logger.info(f"Marked *{full_title} ({year})* as watched on Trakt.")

    logger.info(f"Watched at: {watched_at}")

def mark_as_watched_on_trakt(item):
    """Send a request to Trakt to mark media as watched."""
    if item.get("percent_complete", 0) < 90:
        logger.info(f"Skipping {item.get('full_title')}: not watched >90%")
        return False

    media_ids = get_media_id(item.get("rating_key"))
    if not media_ids:
        logger.warning(f"Could not find a valid ID for rating key {item.get('rating_key')}")
        return False

    watched_at = datetime.fromtimestamp(item["date"], timezone.utc).isoformat()
    payload = {"movies": [], "episodes": []}
    if "tmdb" in media_ids:
        payload["movies"].append({"watched_at": watched_at, "ids": media_ids})
    else:
        payload["episodes"].append({"watched_at": watched_at, "ids": media_ids})

    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": TRAKT_CLIENT_ID,
        "Authorization": f"Bearer {trakt.token['access_token']}",
    }

    response = requests.post("https://api.trakt.tv/sync/history", json=payload, headers=headers)

    if response.status_code == 201:
        log_success(item)  # Log the success after a successful sync
        return True
    else:
        logger.error(f"Failed to mark as watched on Trakt: {response.status_code} - {response.text}")
        return False
