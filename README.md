## HomeBot
- I made this discord bot that connects to an MQTT that receives from an ESP32 when there is motion using an HC-SR501 (code of the ESP32 is in a private repo)
- However you can use this base code to receive message from an MQTT (I use HiveMQ) as it is not configured only for mine.

## JSON
- To connect your MQTT with your discord bot you have to create **config.json** file in the main folder (not src)
  ```
  {
    "DISCORD_TOKEN": "BOT_TOKEN",
    "DISCORD_CHANNEL_ID": "CHANNEL_ID",
    "MQTT_BROKER": "MQTT_BROKER",
    "MQTT_PORT": PORT_INT,
    "MQTT_TOPIC": "YOUR_TOPIC",
    "MQTT_USERNAME": "USERNAME",
    "MQTT_PASSWORD": "PASSWORD"
  }
