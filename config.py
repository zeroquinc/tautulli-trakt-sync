import configparser
import os
from datetime import datetime
from loguru import logger

# Load config
config = configparser.ConfigParser()
config_file = "config.ini"

if not os.path.exists(config_file):
    config["Tautulli"] = {
        "url": "YOUR_TAUTULLI_URL",
        "api_key": "YOUR_TAUTULLI_API_KEY",
        "username": "YOUR_TAUTULLI_USERNAME",
    }
    config["Trakt"] = {
        "client_id": "YOUR_TRAKT_CLIENT_ID",
        "client_secret": "YOUR_TRAKT_CLIENT_SECRET",
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "token_file": "trakt_token.json",
    }
    config["Logging"] = {"level": "INFO"}
    with open(config_file, "w") as configfile:
        config.write(configfile)
    print("Created default config.ini. Please update with your credentials.")
    exit()

config.read(config_file)

# Extract config values
TAUTULLI_URL = config["Tautulli"]["url"]
TAUTULLI_API_KEY = config["Tautulli"]["api_key"]
USERNAME = config["Tautulli"]["username"]
TRAKT_CLIENT_ID = config["Trakt"]["client_id"]
TRAKT_CLIENT_SECRET = config["Trakt"]["client_secret"]
TRAKT_REDIRECT_URI = config["Trakt"]["redirect_uri"]
TOKEN_FILE = config["Trakt"]["token_file"]

# Logging setup
log_level = config.get("Logging", "level", fallback="INFO").upper()
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d_%H") + ".log")
logger.add(log_filename, level=log_level)