import os
import shutil
import configparser
from colorizer import Colorizer  # Assuming Colorizer class is defined in colorizer.py

def verify_dir(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            print(Colorizer("red").colorize("Creation of the directory failed. Terminating."))
            exit(1)

def overwrite_confirmation(directory):
    if os.path.exists(directory):
        response = input(Colorizer("yellow").colorize(
            f"There already seems to be a {directory} directory here. Proceeding will overwrite it COMPLETELY. "
            f"Do you still want to continue (yes/no)? "
        ))
        return response.lower() == 'yes' or response.lower() == 'y'
    return None

def ask(prompt):
    while True:
        response = input(prompt).lower()
        if response in ['yes', 'no', 'y', 'n']:
            return response == 'yes' or response == 'y'
        else:
            print(Colorizer("red").colorize("Invalid input. Please enter 'yes', 'no', 'y', or 'n'."))

def generate_config():
    config_dir = "_config_"
    
    confirmation = overwrite_confirmation(config_dir)
    if not confirmation:
        print(Colorizer("red").colorize("Operation aborted. Configuration generation canceled."))
        return
    elif confirmation is True:
        shutil.rmtree(config_dir)
        print(Colorizer("cyan").colorize("Removed existing configuration directory."))
    elif confirmation is None:
        print(Colorizer("green").colorize("No existing configuration directory found. Creating one."))
    verify_dir(config_dir)

    # Directories configuration
    log_dir = input("Enter the log directory: ")
    verify_dir(log_dir)

    # Types configuration
    dm_enabled = ask("Enable direct messages (yes/no): ")
    dm_download_images = ask("Download images in direct messages (yes/no): ")
    dm_download_videos = ask("Download videos in direct messages (yes/no): ")
    dm_download_audio = ask("Download audio in direct messages (yes/no): ")

    server_enabled = ask("Enable server messages (yes/no): ")
    server_download_images = ask("Download images in server messages (yes/no): ")
    server_download_videos = ask("Download videos in server messages (yes/no): ")
    server_download_audio = ask("Download audio in server messages (yes/no): ")

    # Misc configuration
    print_contents = ask("Print contents (yes/no): ")
    log_to_dms = ask("Enable logging to direct messages (yes/no): ")
    owner_id = int(input("Enter owner ID: "))

    with open(os.path.join(config_dir, "directories.cfg"), "w") as f:
        f.write(f"[directories]\nlog_dir = {log_dir}\n")

    with open(os.path.join(config_dir, "types.cfg"), "w") as f:
        f.write("[direct_messages]\n"
                f"enabled = {dm_enabled}\n"
                f"download_images = {dm_download_images}\n"
                f"download_videos = {dm_download_videos}\n"
                f"download_audio = {dm_download_audio}\n\n"
                f"[servers]\n"
                f"enabled = {server_enabled}\n"
                f"download_images = {server_download_images}\n"
                f"download_videos = {server_download_videos}\n"
                f"download_audio = {server_download_audio}\n")

    with open(os.path.join(config_dir, "misc.cfg"), "w") as f:
        f.write("[Console]\nprintContents = {}\n\n"
                "[DiscordLog]\nenabled = {}\nownerid = {}\n".format(print_contents, log_to_dms, owner_id))

    print(Colorizer("green").colorize("Configuration files generated successfully."))

if __name__ == "__main__":
    generate_config()
