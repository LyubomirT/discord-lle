# Discord: Log Literally Everything
<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.8.0-yellow.svg?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-380/)
[![Py-Cord](https://img.shields.io/badge/Py--Cord-2.0.0-blue.svg?logo=discord&logoColor=white)](https://https://pycord.dev/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-green.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Any OS](https://img.shields.io/badge/OS-Any-red.svg?logo=linux&logoColor=white)


## Overview 📖

Do you want to record everything that happens on your Discord server? You've arrived at the correct location! This bot will log everything in both servers and DMs, from messages to attachments. Everything that happens around you will be recorded and saved to a directory of your choosing.

- Comprehensive logging of messages and attachments in both servers and DMs.
- Customizable logging directory and file format.
- Optional logging to DMs for direct monitoring.
- Interactive configuration generator for ease of setup.


## Installation 💾

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

4. Run `cfg_gen.py` to generate the configuration files:

```bash
python cfg_gen.py
```

5. Create an `.env` file and add the following line:

```bash
BOT_TOKEN = TOKENFROMDISCORD
```

6. Run the bot:

```bash
python main.py
```

### NOTE ⚠

Privileged Gateway Intents must be enabled for this bot. You can enable them by going to the "Bot" page in the Discord Developer Portal. These are essential for the bot to log server messages and deliver messages to DMs.

![image](https://discordpy.readthedocs.io/en/latest/_images/discord_privileged_intents.png)

## Usage 📦

Messages (or message attachments) will be automatically logged to the selected directory by the bot. The directory, on the other hand, must adhere to a specified format:

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

## Configuration ⚙

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

## Log File Format 📝

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

If there is a media attachment, it will also be saved to the directory. The file will be the same MIME type / file extension as the original file. For example, if the attachment is a PNG image, the file will be saved as a PNG image as well. The file name will be in the following format:

```bash
<timestamp>_<message_id>_<type>_<filename>
```

## Logs in DMs 📬

The bot can also send the log files to the owner of the bot. This can be useful if you want to keep track of what the bot is logging. To enable this, set `enabled` to `true` in `_config_/misc.cfg`. You can also change the owner ID in the same file.

The bot will send two messages to the owner when a message is logged. The first one will be the log file itself, and the second one will be a summary of the message. The summary will contain the following information:

- The name and ID of the user that sent the message
- The name and ID of the server that the message was sent in
- The name and ID of the channel that the message was sent in
- The timestamp of the message

Also note that this data may differ between DMs and servers. For example, the server name and ID will not be included in the summary if the message was sent in a DM. (DMs don't have server information after all :P)

## Configuration Generator 🛠

The project comes with an interactive configuration generator that simplifies the process of configuring the bot. To run it, simply run `cfg_gen.py`:

```bash
python cfg_gen.py
```

The configuration generator will ask you a series of questions, basically gathering the same info it would use if you were to configure the bot manually. Once you're done, it will generate the configuration files for you in the `_config_` folder.

Note that the configuration generator will overwrite any existing configuration files if `_config_` already exists. This is to prevent any issues with the configuration files and to avoid making a mess.

## Contributing 🤝

Thank you for considering contributing to this project! If you have any questions, feel free to contact me on Discord at `@lyubomirt`. You can also check out the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.

### Bug Reports 🐛

Please take a look at the issue tracker before submitting a bug report. If you find a bug that hasn't been reported yet, please create a new issue and include as much information as possible. This includes:

- The version of the bot you are using
- The version of Python you are using
- The operating system you are using
- The steps to reproduce the bug
- Any other information that may be useful

### Pull Requests 📥

Pull requests are welcome! If you want to contribute to this project, please follow the steps below (and make sure to read the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information):

1. Fork the repository
2. Clone the repository
3. Make your changes (locally)
4. Commit your changes to your fork
5. Push your changes to your fork
6. Create a pull request on the original repository
7. Explain your changes and why they should be merged
8. Wait for a response :D

## Discord Server 📡

If you have any questions, suggestions, or just want to hang out, feel free to join the official [Discord server](https://discord.gg/4nVVhh29E3) of the developer!

## License 📜

This project is licensed under the [BSD 3-Clause License](LICENSE). Please abide by the terms of the license when using this project. Thank you! ♥

## Acknowledgements 🙏

Special thanks to the developers of the libraries used in this project! Without their hard work, this project would not be possible.




