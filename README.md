<!--
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

token = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
log_dir = "_logs_"

dm_config = {
    "enabled": True,
    "download_images": True,
    "download_videos": True,
    "download_audio": True,
}

server_config = {
    "enabled": True,
    "download_images": True,
    "download_videos": True,
    "download_audio": True,
}

printContents = False

logtodms = False
ownerid = 0

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
        global server_config
        server_config["enabled"] = bool(config["servers"]["enabled"])
        server_config["download_images"] = bool(config["servers"]["download_images"])
        server_config["download_videos"] = bool(config["servers"]["download_videos"])
        server_config["download_audio"] = bool(config["servers"]["download_audio"])
    with open("_config_/misc.cfg", "r") as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        global printContents
        printContents = bool(config["Console"]["printContents"])
        global logtodms
        logtodms = bool(config["DiscordLog"]["enabled"])
        global ownerid
        ownerid = int(config["DiscordLog"]["ownerid"])
    
    
    verify_dir(log_dir)
        

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
                file = discord.File(log_file_path)
                await bot.get_user(ownerid).send(file=file)
                """
                await bot.get_user(ownerid).send("Log file for " + message.author.name + " (" + str(message.author.id) + ")")
                await bot.get_user(ownerid).send("Message ID: " + str(message.id))
                await bot.get_user(ownerid).send("Message Content: " + message.content)
                await bot.get_user(ownerid).send("Message Timestamp: " + str(message.created_at))
                await bot.get_user(ownerid).send("Message Author: " + str(message.author.name) + " (" + str(message.author.id) + ")")
                """
                # Put all of the above into a single message
                await bot.get_user(ownerid).send(f"""Log file for {message.author.name} ({str(message.author.id)})
Message ID: {str(message.id)}
Message Timestamp: {str(message.created_at)}
Message Author: {str(message.author.name)} ({str(message.author.id)})""")
                


                    
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
            file = discord.File(log_file_path)
            await bot.get_user(ownerid).send(file=file)
            """
            await bot.get_user(ownerid).send("Log file for " + message.author.name + " (" + str(message.author.id) + ")")
            await bot.get_user(ownerid).send("Message ID: " + str(message.id))
            await bot.get_user(ownerid).send("Message Guild: " + str(message.guild.name) + " (" + str(message.guild.id) + ")")
            await bot.get_user(ownerid).send("Message Timestamp: " + str(message.created_at))
            await bot.get_user(ownerid).send("Message Channel: " + str(message.channel) + " (" + str(message.channel.id) + ")")
            await bot.get_user(ownerid).send("Message Author: " + str(message.author.name) + " (" + str(message.author.id) + ")")
            """
            # Put all of the above into a single message
            await bot.get_user(ownerid).send(f"""Log file for {message.author.name} ({str(message.author.id)})
Message ID: {str(message.id)}
Message Guild: {str(message.guild.name)} ({str(message.guild.id)})
Message Timestamp: {str(message.created_at)}
Message Channel: {str(message.channel)} ({str(message.channel.id)})
Message Author: {str(message.author.name)} ({str(message.author.id)})""")




bot.remove_command("help")

bot.run(token)


 -->

# Discord: Log Literally Everything

This is a project that I made to log messages from a Discord server or a DM to a specified directory. It's useful for saving stuff for long-term storage, or for archiving a server without having to re-print every single message. 

## Installation

1. Clone the repository:

```bash
git clone https://github.com/LyubomirT/discord-lle.git
```

2. Switch to the directory:

```bash
cd discord-lle
```

3. Install the requirements:

```bash
pip install -r requirements.txt
```

4. Configure the bot by editing the files in the `_config_` folder.

5. Run the bot:

```bash
python main.py
```

## Usage

The bot will automatically log messages (or message attachments) to the specified directory. The directory, however, must follow a specific format:

```
DMs
    - <username>
        - <timestamp>_<message_id>.txt
Servers
    - <server_name>
        - <channel_name>
            - <timestamp>_<message_id>.txt
```

The bot will automatically create the directories if they don't exist.

## Configuration

The bot can be configured by editing the files in the `_config_` folder. The configuration files are as follows:

### `_config_/directories.cfg`

This file contains the directory that the bot will log to. By default, it is set to `logs`. You can change this to whatever you want.

Example:

```cfg
[directories]
log_dir=F:\VSCODE-PROJECTS\discord-lle\logs
```

### `_config_/types.cfg`

In this file, you can configure what kind of messages the bot will log. By default, the bot will log everything from both DMs and servers. The bot also will by default download images, videos, and audio files.

Example:

```cfg
[direct_messages]
enabled = true
download_images = true
download_videos = true
download_audio = true

[servers]
enabled = true
download_images = true
download_videos = true
download_audio = true
```

`enabled` determines whether or not the bot will log messages from that source. `download_images`, `download_videos`, and `download_audio` determine whether or not the bot will download those types of attachments.

### `_config_/misc.cfg`

This file contains miscellaneous configuration options. For example, you can enable or disable printing the contents of the log files to the console, or you can enable or disable logging to DMs. You can also change the owner ID, which is the ID of the user that will receive the log files if logging to DMs is enabled.

Example:

```cfg
[Console]
printContents = true

[DiscordLog]
enabled = true
ownerid = 861620168370683924
```

## Log File Format

Each log file will consist of the following information below "keys" that are enclosed in square brackets. The keys are as follows:

- `[Message]` - The message content
- `[Image Attachment]` - The path to the image attachment
- `[Video Attachment]` - The path to the video attachment
- `[Audio Attachment]` - The path to the audio attachment

Example:

```
[Message]
Hello, world!

[Image Attachment]
F:\VSCODE-PROJECTS\discord-lle\logs\DMs\fdhfdhfdh_ididididid\timetimetime_messageidmessageid_image_image.png
```

If there was a media attachment, it will also be saved to the directory. The file will be the same MIME type / file extension as the original file. For example, if the attachment was a PNG image, the file will be saved as a PNG image. The file name will be in the following format:

```bash
<timestamp>_<message_id>_<type>_<filename>
```

## Logs in DMs

The bot can also send the log files to the owner of the bot. This can be useful if you want to keep track of what the bot is logging. To enable this, set `enabled` to `true` in `_config_/misc.cfg`. You can also change the owner ID in the same file.

The bot will send two messages to the owner when a message is logged. The first one will be the log file itself, and the second one will be a summary of the message. The summary will contain the following information:

- The name and ID of the user that sent the message
- The name and ID of the server that the message was sent in
- The name and ID of the channel that the message was sent in
- The timestamp of the message

Also note that this data may differ between DMs and servers. For example, the server name and ID will not be included in the summary if the message was sent in a DM. (DMs don't have server information after all :P)




