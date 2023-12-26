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
from verify_dir import verify_dir


load_dotenv()

# Intitialize Global Vars
token = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

log_dir: str = None

dm_config: dict = None
server_config: dict = None

printContents: bool = None
logtodms: bool = None
ownerid: int = None

def load_config_dirs():
    with open("_config_/directories.cfg", "r") as f:
        try:
            config = configparser.ConfigParser()
            config.read_file(f)

            log_dir = config["directories"]["log_dir"]
            verify_dir(log_dir)
            return log_dir
        except KeyError:
            print(Colorizer("red").colorize("Could not load config! Please specify a proper log directory or use cfg_gen.py to generate a new config file."))
            os._exit(1)
        except Exception:
            print(Colorizer("red").colorize(f"Could not load config! The directories.cfg file is missing or corrupt."))
            os._exit(1)

def load_config_types():
    with open("_config_/types.cfg", "r") as f:
        try:
            dm_config = {}
            server_config = {}

            config = configparser.ConfigParser()
            config.read_file(f)

            step = 0
            dm_config["enabled"] = bool(config["direct_messages"]["enabled"])
            dm_config["download_images"] = bool(config["direct_messages"]["download_images"])
            dm_config["download_videos"] = bool(config["direct_messages"]["download_videos"])
            dm_config["download_audio"] = bool(config["direct_messages"]["download_audio"])

            step = 1
            server_config["enabled"] = bool(config["servers"]["enabled"])
            server_config["download_images"] = bool(config["servers"]["download_images"])
            server_config["download_videos"] = bool(config["servers"]["download_videos"])
            server_config["download_audio"] = bool(config["servers"]["download_audio"])

            return dm_config, server_config

        except KeyError:
            errorType = ('DM', 'server')
            print(Colorizer("red").colorize(f"Could not load config! Please specify proper types ({errorType[step]}) or use cfg_gen.py to generate a new config file."))
            os._exit(1)
        except Exception:
            print(Colorizer("red").colorize("Could not load config! The types.cfg file is missing or corrupt."))
            os._exit(1)

def load_config_misc():
    with open("_config_/misc.cfg", "r") as f:
        try:
            config = configparser.ConfigParser()
            config.read_file(f)

            step = 0
            printContents = bool(config["Console"]["printContents"])

            step = 1
            logtodms = bool(config["DiscordLog"]["enabled"])

            step = 2
            ownerid = int(config["DiscordLog"]["ownerid"])

            return printContents, logtodms, ownerid

        except KeyError:
            miscOptions = ('printContents', 'logtodms', 'ownerid')
            print(Colorizer("red").colorize(f"Could not load config! Please specify proper misc options ({miscOptions[step]}) or use cfg_gen.py to generate a new config file."))
            os._exit(1)
        except Exception:
            print(Colorizer("red").colorize("Could not load config! The misc.cfg file is missing or corrupt."))
            os._exit(1)

@bot.event
async def on_ready():
    global log_dir
    global dm_config
    global server_config
    global printContents
    global logtodms
    global ownerid

    # Assign globals from loading configs
    log_dir = load_config_dirs()

    config_types = load_config_types()
    dm_config = config_types[0]
    server_config = config_types[1]

    config_misc = load_config_misc()
    printContents = config_misc[0]
    logtodms = config_misc[1]
    ownerid = config_misc[2]

    # Check if all privileged intents are enabled, else raise error and quit
    if not all((bot.intents.presences, bot.intents.members, bot.intents.message_content)):
        print(Colorizer("red").colorize("One or more privileged intents are not enabled! Privilege intents include GUILD_PRESENCES, GUILD_MEMBERS, MESSAGE_CONTENT."))
        os._exit(1)

    print(Colorizer("cyan").colorize("Bot is ready! Using configuration provided in the _config_ folder."))
    print(Colorizer("yellow").colorize("Bot is running on version 1.0.0"))
    print(Colorizer("yellow").colorize("Config Preview:"))

    print(Colorizer("yellow").colorize("Log directory: " + log_dir))
    print(Colorizer("purple").colorize("Direct Messages:"))
    print(Colorizer("purple").colorize("Enabled: " + str(dm_config["enabled"])))
    print(Colorizer("purple").colorize("Download Images: " + str(dm_config["download_images"])))
    print(Colorizer("purple").colorize("Download Videos: " + str(dm_config["download_videos"])))
    print(Colorizer("purple").colorize("Download Audio: " + str(dm_config["download_audio"])))
    print(Colorizer("cyan").colorize("Servers:"))
    print(Colorizer("cyan").colorize("Enabled: " + str(server_config["enabled"])))
    print(Colorizer("cyan").colorize("Download Images: " + str(server_config["download_images"])))
    print(Colorizer("cyan").colorize("Download Videos: " + str(server_config["download_videos"])))
    print(Colorizer("cyan").colorize("Download Audio: " + str(server_config["download_audio"])))
    print(Colorizer("yellow").colorize("Misc:"))
    print(Colorizer("yellow").colorize("Print Contents: " + str(printContents)))
    print(Colorizer("yellow").colorize("Log to DMs: " + str(logtodms)))
    print(Colorizer("yellow").colorize("Owner ID: " + str(ownerid)))


# LOG DIRECTORY MUST EITHER BE EMPTY OR FOLLOW THIS FORMAT:
# DMs
#   - <username>
#       - <timestamp>_<message_id>.txt
# Servers
#   - <server_name>
#       - <channel_name>
#           - <timestamp>_<message_id>.txt

async def send_log_to_dm(log_file_path: str, message: discord.Message):
    file = discord.File(log_file_path)
    user: discord.User = await bot.get_user(ownerid)
    if isinstance(user, discord.User):
        await user.send(file=file)

        lines = [f"Log file for {message.author.name} ({message.author.id})",
                f"Message ID: {message.id}",
                f"Message Content: {message.content}",
                f"Message Timestamp: {message.created_at}"
                f"Message Author: {message.author.name} ({message.author.id})"]

        await user.send("\n".join(lines))

# When a DM message is received, this event will be triggered.
@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    
    # Check if the message is a DM
    if isinstance(message.channel, discord.channel.DMChannel):
        # Check if DM logging is enabled
        if dm_config["enabled"]:
            # Check if the user has a directory
            user_dir = log_dir + "/DMs/" + message.author.name + "_" + str(message.author.id)
            if not os.path.exists(user_dir):
                os.mkdir(user_dir)
            
            # Define the log file path
            log_file_path = f"{user_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}_text.txt"
            
            # Check if the message content is not empty
            if message.content.strip():
                # Create the file
                with open(log_file_path, "w", encoding='utf-8') as f:
                    # Write the message contents to the file
                    f.write("[Message]\n" + message.content + "\n")
            
            # Check if the user wants to download images
            if dm_config["download_images"] and message.attachments:
                image_attachment = message.attachments[0]
                # Check if the attachment is an image
                if "image" in image_attachment.content_type:
                    image_path = f"{user_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}_image_{image_attachment.filename}"
                    await image_attachment.save(image_path)
                    # Update the log file with image information
                    with open(log_file_path, "a", encoding='utf-8') as f:
                        f.write(f"[Image Attachment]\n{image_path}\n")
            
            # Check if the user wants to download videos
            if dm_config["download_videos"] and message.attachments:
                video_attachment = message.attachments[0]
                # Check if the attachment is a video
                if "video" in video_attachment.content_type:
                    video_path = f"{user_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}_video_{video_attachment.filename}"
                    await video_attachment.save(video_path)
                    # Update the log file with video information
                    with open(log_file_path, "a", encoding='utf-8') as f:
                        f.write(f"[Video Attachment]\n{video_path}\n")
            
            # Check if the user wants to download audio
            if dm_config["download_audio"] and message.attachments:
                audio_attachment = message.attachments[0]
                # Check if the attachment is an audio file
                if "audio" in audio_attachment.content_type:
                    audio_path = f"{user_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}_audio_{audio_attachment.filename}"
                    await audio_attachment.save(audio_path)
                    # Update the log file with audio information
                    with open(log_file_path, "a", encoding='utf-8') as f:
                        f.write(f"[Audio Attachment]\n{audio_path}\n")
            
            # If printContents is enabled, print the contents of the log file
            if printContents:
                with open(log_file_path, "r", encoding='utf-8') as f:
                    # ========= DATETIME =========\n\nCONTENTS\n\n==============================
                    print(Colorizer("yellow").colorize(f"========== {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')} ==========\n\n{f.read()}\n\n=============================="))
            
            # If logtodms is enabled, send the log file to the owner
            if logtodms:
                await send_log_to_dm(log_file_path, message)

    elif isinstance(message.channel, discord.channel.TextChannel):
        if not server_config["enabled"]:
            return
        # Check if the server has a directory
        server_dir = log_dir + "/Servers/" + message.guild.name + "_" + str(message.guild.id)
        if not os.path.exists(server_dir):
            os.mkdir(server_dir)
        
        # Check if the channel has a directory
        channel_dir = server_dir + "/" + message.channel.name + "_" + str(message.channel.id)
        if not os.path.exists(channel_dir):
            os.mkdir(channel_dir)
        
        # Define the log file path
        log_file_path = f"{channel_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}_text.txt"
        
        # Check if the message content is not empty
        if message.content.strip():
            # Create the file
            with open(log_file_path, "w", encoding='utf-8') as f:
                # Write the message contents to the file
                f.write("[Message]\n" + message.content + "\n")
        
        # Check if the user wants to download images
        if server_config["download_images"] and message.attachments:
            image_attachment = message.attachments[0]
            # Check if the attachment is an image
            if "image" in image_attachment.content_type:
                image_path = f"{channel_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}_image_{image_attachment.filename}"
                await image_attachment.save(image_path)
                # Update the log file with image information
                with open(log_file_path, "a", encoding='utf-8') as f:
                    f.write(f"[Image Attachment]\n{image_path}\n")
        
        # Check if the user wants to download videos
        if server_config["download_videos"] and message.attachments:
            video_attachment = message.attachments[0]
            # Check if the attachment is a video
            if "video" in video_attachment.content_type:
                video_path = f"{channel_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}_video_{video_attachment.filename}"
                await video_attachment.save(video_path)
                # Update the log file with video information
                with open(log_file_path, "a", encoding='utf-8') as f:
                    f.write(f"[Video Attachment]\n{video_path}\n")
        
        # Check if the user wants to download audio
        if server_config["download_audio"] and message.attachments:
            audio_attachment = message.attachments[0]
            # Check if the attachment is an audio file
            if "audio" in audio_attachment.content_type:
                audio_path = f"{channel_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}_audio_{audio_attachment.filename}"
                await audio_attachment.save(audio_path)
                # Update the log file with audio information
                with open(log_file_path, "a", encoding='utf-8') as f:
                    f.write(f"[Audio Attachment]\n{audio_path}\n")

        
        # If printContents is enabled, print the contents of the log file
        if printContents:
            with open(log_file_path, "r", encoding='utf-8') as f:
                # ========= DATETIME =========\n\nCONTENTS\n\n==============================
                print(Colorizer("yellow").colorize(f"========== {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')} ==========\n\n{f.read()}\n\n=============================="))

        # If logtodms is enabled, send the log file to the owner
        if logtodms:
            await send_log_to_dm(log_file_path, message)

bot.remove_command("help")

bot.run(token)

