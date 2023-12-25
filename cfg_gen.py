import os
import shutil
import configparser
from colorizer import Colorizer

def verify_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def overwrite_confirmation(directory):
    if os.path.exists(directory):
        response = input(Colorizer("yellow").colorize(
            f"There already seems to be a {directory} directory here. Proceeding will overwrite it COMPLETELY. "
            f"Do you still want to continue (y/n)? "
        ))
        return response.lower() == 'y'
    return True

def generate_config():
    config_dir = "_config_"
    
    if not overwrite_confirmation(config_dir):
        print(Colorizer("red").colorize("Operation aborted. Configuration generation canceled."))
        return
    
    verify_dir(config_dir)

    # Directories configuration
    log_dir = input("Enter the log directory: ")
    verify_dir(log_dir)

    # Types configuration
    dm_enabled = input("Enable direct messages (True/False): ").lower() == 'true'
    dm_download_images = input("Download images in direct messages (True/False): ").lower() == 'true'
    dm_download_videos = input("Download videos in direct messages (True/False): ").lower() == 'true'
    dm_download_audio = input("Download audio in direct messages (True/False): ").lower() == 'true'

    server_enabled = input("Enable server messages (True/False): ").lower() == 'true'
    server_download_images = input("Download images in server messages (True/False): ").lower() == 'true'
    server_download_videos = input("Download videos in server messages (True/False): ").lower() == 'true'
    server_download_audio = input("Download audio in server messages (True/False): ").lower() == 'true'

    # Misc configuration
    print_contents = input("Print contents (True/False): ").lower() == 'true'
    log_to_dms = input("Enable logging to direct messages (True/False): ").lower() == 'true'
    owner_id = int(input("Enter owner ID: "))

    # Write configuration to files
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
        f.write("[Console]\nprintContents = {print_contents}\n\n"
                "[DiscordLog]\nenabled = {log_to_dms}\nownerid = {owner_id}\n")

    print(Colorizer("green").colorize("Configuration files generated successfully."))

if __name__ == "__main__":
    generate_config()
