import os
import shutil
from colorizer import Colorizer  # Assuming Colorizer class is defined in colorizer.py


def create_dir(directory: str) -> bool:
    try:
        os.makedirs(directory)
    except OSError:
        print(Colorizer("red").colorize("Creation of the directory failed. Terminating."))
        return False
    return True

def overwrite_confirmation(directory: str) -> bool:
    response = input(Colorizer("yellow").colorize(
        f"There already seems to be a {directory} directory here. Proceeding will overwrite it COMPLETELY. "
        f"Do you still want to continue (yes/no)? "))
    
    if response[0].lower() == "y":
        return True
    
    print(response[0])
    return False

def config_options() -> dict:
    options = {
        "Enable direct messages (yes/no): " : False,
        "Download images in direct messages (yes/no): " : False,
        "Download videos in direct messages (yes/no): " : False,
        "Download audio in direct messages (yes/no): " : False,

        "Enable server messages (yes/no): " : False,
        "Download images in server messages (yes/no): " : False,
        "Download videos in server messages (yes/no): " : False,
        "Download audio in server messages (yes/no): " : False,

        "Print contents (yes/no): " : False,
        "Enable logging to direct messages (yes/no): " : False,
        "Enter owner ID: " : 6969,
    }

    for option in options:
        options[option] = ask(option) if "owner" not in option else ask(option, type=int)
            
    return options

def config_push(directory: str, log_directory: str, options: dict) -> bool:
    config_files = ["directories.cfg", "types.cfg", "misc.cfg"]

    for file in config_files:
        with open(os.path.join(directory, file), "w") as f:

            if "directories" in file:
                f.write(f"[directories]\nlog_dir = {log_directory}\n")

            if "types" in file:
                f.write("[direct_messages]\n"
                        f"enabled = {options['Enable direct messages (yes/no): ']}\n"
                        f"download_images = {options['Download images in direct messages (yes/no): ']}\n"
                        f"download_videos = {options['Download videos in direct messages (yes/no): ']}\n"
                        f"download_audio = {options['Download audio in direct messages (yes/no): ']}\n\n"
                        f"[servers]\n"
                        f"enabled = {options['Enable server messages (yes/no): ']}\n"
                        f"download_images = {options['Download images in server messages (yes/no): ']}\n"
                        f"download_videos = {options['Download videos in server messages (yes/no): ']}\n"
                        f"download_audio = {options['Download audio in server messages (yes/no): ']}\n")
                
            if "misc" in file:
                    f.write("[Console]\nprintContents = {}\n\n"
                        "[DiscordLog]\nenabled = {}\nownerid = {}\n".format(options['Print contents (yes/no): '],
                                                options['Enable logging to direct messages (yes/no): '], options['Enter owner ID: ']))
    
    return True

def ask(prompt: str, type=str) -> bool | int:
    while True:
        try:
            response = type(input(prompt).lower())

        except ValueError:
            print(Colorizer("red").colorize("Invalid input. Please try again!"))
            continue

        if response in ['yes', 'no', 'y', 'n']:
            return response == 'yes' or response == 'y'
        
        if type is int:
            return response
        
        print(Colorizer("red").colorize("Invalid input. Please enter 'yes', 'no', 'y', or 'n'."))

def generate_config() -> bool | None:
    config_dir = "_config_"

    if os.path.exists(config_dir):
        if not overwrite_confirmation(config_dir):
            print(Colorizer("red").colorize("Operation aborted. Configuration generation canceled."))
            return None
        
        shutil.rmtree(config_dir)

    if not create_dir(config_dir):
        return None
    
    log_dir = input("Enter the log directory: ")

    if os.path.exists(log_dir):
        if not overwrite_confirmation(log_dir):
            print(Colorizer("red").colorize("Operation aborted. Configuration generation canceled."))
            return None
        
        shutil.rmtree(log_dir)

    if not create_dir(log_dir):
        return None
    
    options = config_options()

    if not config_push(config_dir, log_dir, options):
        print("Error")
        return None
    
    print(Colorizer("green").colorize("Configuration files generated successfully."))
    return True

if __name__ == "__main__":
    generate_config()
