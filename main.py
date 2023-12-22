from dotenv import load_dotenv
import os
import requests
import json
import discord
from discord.ext import commands
from discord.commands import Option
from discord.ui import Button, View, Select, Modal
from colorizer import Colorizer
import configparser
import asyncio
from datetime import datetime

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="!")
log_dir = "_logs_"

dm_config = {
    "enabled": True,
    "download_images": True,
    "download_videos": True,
    "download_audio": True,
}

def load_config():
    with open("_config_/directories.cfg", "r") as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        global log_dir
        log_dir = config["directories"]["log_dir"]
    with open("_config_/types.cfg", "r") as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        global dm_config
        dm_config["enabled"] = bool(config["direct_messages"]["enabled"])
        dm_config["download_images"] = bool(config["direct_messages"]["download_images"])
        dm_config["download_videos"] = bool(config["direct_messages"]["download_videos"])
        dm_config["download_audio"] = bool(config["direct_messages"]["download_audio"])
    
    verify_dir()


def verify_dir():
    # Fully verify the directory structure
    # If it doesn't exist, create it
    # If it does exist, make sure it is empty or follows the correct format

    # Check if the log directory exists
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
        print(Colorizer("cyan").colorize("Log directory created."))
    else:
        print(Colorizer("cyan").colorize("Log directory already exists."))
    
    # Check if the DM directory exists
    if not os.path.exists(log_dir + "/DMs"):
        os.mkdir(log_dir + "/DMs")
    
    # Check if the server directory exists
    if not os.path.exists(log_dir + "/Servers"):
        os.mkdir(log_dir + "/Servers")

    # Check if the DM directory is empty
    if not os.listdir(log_dir + "/DMs"):
        print(Colorizer("cyan").colorize("DM directory is empty."))
    else:
        print(Colorizer("cyan").colorize("DM directory is not empty."))
    
    # Check if the server directory is empty
    if not os.listdir(log_dir + "/Servers"):
        print(Colorizer("cyan").colorize("Server directory is empty."))
    else:
        print(Colorizer("cyan").colorize("Server directory is not empty."))
        

@bot.event
async def on_ready():
    print(Colorizer("cyan").colorize("Bot is ready! Using configuration provided in the _config_ folder."))
    print(Colorizer("yellow").colorize("Bot is running on version 1.0.0"))
    print(Colorizer("yellow").colorize("Config Preview:"))
    load_config()
    print(Colorizer("yellow").colorize("Log directory: " + log_dir))
    print(Colorizer("purple").colorize("Direct Messages:"))
    print(Colorizer("purple").colorize("Enabled: " + str(dm_config["enabled"])))
    print(Colorizer("purple").colorize("Download Images: " + str(dm_config["download_images"])))
    print(Colorizer("purple").colorize("Download Videos: " + str(dm_config["download_videos"])))
    print(Colorizer("purple").colorize("Download Audio: " + str(dm_config["download_audio"])))


# LOG DIRECTORY MUST EITHER BE EMPTY OR FOLLOW THIS FORMAT:
# DMs
#   - <username>
#       - <timestamp>_<message_id>.txt
# Servers
#   - <server_name>
#       - <channel_name>
#           - <timestamp>_<message_id>.txt

# When a DM message is received, this event will be triggered.
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Check if the message is a DM
    if isinstance(message.channel, discord.channel.DMChannel):
        # Check if DM logging is enabled
        if dm_config["enabled"]:
            # Check if the user has a directory
            if not os.path.exists(log_dir + "/DMs/" + str(message.author)):
                os.mkdir(log_dir + "/DMs/" + str(message.author))
            # Check if the user has a file
            if not os.path.exists(log_dir + "/DMs/" + str(message.author) + "/" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + "_" + str(message.id) + ".txt"):
                with open(log_dir + "/DMs/" + str(message.author) + "/" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + "_" + str(message.id) + ".txt", "w") as f:
                    f.write("Author: " + str(message.author) + "\n")
                    f.write("Content: " + str(message.content) + "\n")
                    f.write("Attachments: " + str(message.attachments) + "\n")
                    f.write("Created At: " + str(message.created_at) + "\n")
                    f.write("Edited At: " + str(message.edited_at) + "\n")
                    f.write("ID: " + str(message.id) + "\n")
                    f.write("Jump URL: " + str(message.jump_url) + "\n")
                    f.write("Reference: " + str(message.reference) + "\n")
                    f.write("Type: " + str(message.type) + "\n")
                    f.write("Webhook ID: " + str(message.webhook_id) + "\n")
                    f.write("Mentions: " + str(message.mentions) + "\n")
                    f.write("Mention Roles: " + str(message.mention_roles) + "\n")
                    f.write("Pinned: " + str(message.pinned) + "\n")
                    f.write("TTS: " + str(message.tts) + "\n")
                    f.write("Flags: " + str(message.flags) + "\n")
                    f.write("Activity: " + str(message.activity) + "\n")
                    f.write("Application: " + str(message.application) + "\n")



bot.remove_command("help")

bot.run(token)

