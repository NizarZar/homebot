import threading
from bot import run_discord_bot, start_mqtt_client

if __name__ == '__main__':
    threading.Thread(target=run_discord_bot, daemon=True).start()
    start_mqtt_client()