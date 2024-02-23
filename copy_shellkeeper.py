#!/usr/bin/env python3

import shutil
import os

username = "fredrik"  # Replace with your username

# Source and destination paths
source_path = f'/home/{username}/workspace/python_workspace/shellkeeper/shellkeeper.py'
destination_path = '/usr/local/bin/shellkeeper'

def copy_and_make_executable(source, destination):
    try:
        # Copy the file and remove the .py extension
        shutil.copy(source, destination)

        # Make the new file executable
        os.chmod(destination, 0o755)  # Sets the executable permissions

        print(f"Successfully copied and made executable: {destination}")
    except PermissionError:
        print("Permission denied. You might need to run this script as superuser (sudo).")
    except Exception as e:
        print(f"An error occurred: {e}")

copy_and_make_executable(source_path, destination_path)
