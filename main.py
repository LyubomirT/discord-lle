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



bot.remove_command("help")

bot.run(token)

