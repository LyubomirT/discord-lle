import os
from colorizer import Colorizer

def verify_dir(log_dir):
    # Fully verify the directory structure
    # If it doesn't exist, create it
    # If it does exist, make sure it is empty or follows the correct format

    # Check if the log directory exists
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
        print(Colorizer("cyan").colorize("Log directory created."))
    else:
        print(Colorizer("cyan").colorize("Log directory already exists. In use."))
    
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
        print(Colorizer("cyan").colorize("DM directory contains log files / other files."))
    
    # Check if the server directory is empty
    if not os.listdir(log_dir + "/Servers"):
        print(Colorizer("cyan").colorize("Server directory is empty."))
    else:
        print(Colorizer("cyan").colorize("Server directory contains log files / other files."))