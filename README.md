
# Tautulli to Trakt Sync

This script syncs your Tautulli watch history to Trakt, ensuring that recently watched media is correctly marked as watched on Trakt. It is designed to run automatically every hour via a cron job.

## Why?

- **More reliable than live scrobbling**: Trakt scrobbling can be unreliable, sometimes missing plays.
- **Handles repeat plays correctly**: Unlike plextraktsync, this script ensures multiple plays are properly tracked.
- **Automates syncing**: No need for manual intervention; just schedule it with cron.

## Installation

### Requirements

- Python 3
- Pip dependencies:
  ```bash
  pip install requests requests-oauthlib loguru
  ```

### Setup

1. Clone this repository and navigate into the folder:
   ```bash
   git clone https://github.com/your-repo/tautulli-trakt-sync.git
   cd tautulli-trakt-sync
   ```

2. Create and configure `config.ini` (this will be auto-generated on first run if missing):

   ```ini
   [Tautulli]
   url = YOUR_TAUTULLI_URL
   api_key = YOUR_TAUTULLI_API_KEY
   username = YOUR_TAUTULLI_USERNAME

   [Trakt]
   client_id = YOUR_TRAKT_CLIENT_ID
   client_secret = YOUR_TRAKT_CLIENT_SECRET
   redirect_uri = urn:ietf:wg:oauth:2.0:oob
   token_file = trakt_token.json

   [Logging]
   level = INFO
   ```

3. Run the script manually for the first time to authenticate with Trakt:
   ```bash
   python main.py
   ```
   This will prompt you to visit a Trakt URL and enter a code.

4. Once authorized, your Trakt token will be saved locally.

### Automate with Cron

To sync every hour, add the following line to your crontab (`crontab -e`):

```bash
0 * * * * /usr/bin/python3 /path/to/tautulli-trakt-sync/main.py
```

This will run the script at the start of every hour.

### Notes

- Ensure the script has access to your `trakt_token.json` and `config.ini`.
- If your Trakt token expires, the script will attempt to refresh it automatically.
- You can check logs in the `logs/` directory.

# To-do

- Multiple users
- More configuration options

PR's are welcome.