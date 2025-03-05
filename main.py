from tautulli import get_recently_watched
from trakt import refresh_trakt_token, mark_as_watched_on_trakt
from loguru import logger

def sync_watched():
    refresh_trakt_token()
    for item in get_recently_watched():
        if mark_as_watched_on_trakt(item):
            logger.info(f"Successfully synced: {item.get('rating_key')}")

if __name__ == "__main__":
    sync_watched()