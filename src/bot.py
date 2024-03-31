
# enable TLS client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
import discord
import threading
import asyncio
import json
import os
import paho.mqtt.client as paho
from paho import mqtt

client = paho.Client()

# find the directory of config.json
current_config_dir = os.path.dirname(os.path.abspath(__file__))
n_config_path = os.path.join(current_config_dir, '..', 'config.json')

config_path = os.path.normpath(n_config_path)

with open(config_path, 'r') as config_file:
    config = json.load(config_file)

# extract from config.json necessary information
DISCORD_TOKEN = config["DISCORD_TOKEN"]
DISCORD_CHANNEL_ID = int(config["DISCORD_CHANNEL_ID"])
MQTT_BROKER = config["MQTT_BROKER"]
MQTT_PORT = int(config["MQTT_PORT"])
MQTT_TOPIC_ALARM = config["MQTT_TOPIC_ALARM"]
MQTT_TOPIC_TEMPERATURE_ROOM1 = config["MQTT_TOPIC_TEMPERATURE_ROOM1"]
MQTT_TOPIC_REQUEST = config["MQTT_TOPIC_REQUEST"]
MQTT_USERNAME = config["MQTT_USERNAME"]
MQTT_PASSWORD = config["MQTT_PASSWORD"]

# create discord client
intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

async def send_message(message, user_message, is_private):
    try:
        response = user_message
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# when discord client connects
@discord_client.event
async def on_ready():
    global target_channel
    print(f'Logged in as {discord_client.user}')
    target_channel = discord_client.get_channel(DISCORD_CHANNEL_ID)

# send message to the channel event
@discord_client.event
async def send_message_to_discord(content):
    if target_channel:
        await target_channel.send(content)

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return
    username = str(message.author)
    user_message = str(message.content)

    if user_message == '!temp':
        client.publish(MQTT_TOPIC_REQUEST, "TempRequest")
        print("Request sent to MQTT for temperature")

# mqtt connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_ALARM)
    client.subscribe(MQTT_TOPIC_TEMPERATURE_ROOM1)

# check if mqtt sent a message
def on_message_mqtt(client, userdata, msg):
    message = f"**{msg.topic}:** {msg.payload.decode()}"
    print(message)
    if discord_client.is_ready():
        asyncio.run_coroutine_threadsafe(send_message_to_discord(message), discord_client.loop)
def on_publish(client, userdata, mid, properties=None):
    print("published: " + str(mid))

# logs for mqtt (debug)
def on_log(client, userdata, level, buf):
    print("Log: ", buf)


        

def start_mqtt_client():
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_log = on_log
    client.on_connect = on_connect
    client.on_message = on_message_mqtt
    client.on_publish = on_publish
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()

def run_discord_bot():
    discord_client.run(DISCORD_TOKEN)