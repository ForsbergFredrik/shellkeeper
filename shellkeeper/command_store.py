
from dataclasses import dataclass, field
from typing import Dict
import os
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Get the user's home directory
home_dir = os.path.expanduser("~")
store_dir = os.path.join(home_dir, ".shellkeeper")
store_file = os.path.join(store_dir, "store.json")

# Ensure the directory exists
os.makedirs(store_dir, exist_ok=True)


@dataclass
class CommandStore:
    commands: Dict[str, Dict[str, str]] = field(default_factory=dict)

    def load(self):
        if os.path.exists(store_file):
            with open(store_file, 'r') as file:
                try:
                    data = json.load(file)
                    if not isinstance(data, dict):
                        raise ValueError(
                            "Invalid format: Expected a dictionary.")
                    for category, commands in data.items():
                        if not isinstance(commands, dict):
                            raise ValueError(
                                "Invalid format: Expected a dictionary.")
                        for name, command in commands.items():
                            if not isinstance(name, str) or not isinstance(command, str):
                                raise ValueError(
                                    "Invalid format: Expected string values.")
                        self.commands = data
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error: {e}. Starting with an empty structure.")
                    self.commands = {}
        else:
            self.commands = {}

    def save(self):
        with open(store_file, 'w') as file:
            json.dump(self.commands, file, indent=4)

    def add_command(self, category: str, name: str, command: str):
        if category not in self.commands:
            self.commands[category] = {}
        self.commands[category][name] = command
        self.save()
        print(f'Command "{name}" added successfully.')

    def delete_command(self, name: str):
        for category in list(self.commands.keys()):
            if name in self.commands[category]:
                print(
                    f'Command: {name} in category {category} deleted successfully.')
                del self.commands[category][name]

                # If category is now empty, remove it
                if not self.commands[category]:
                    del self.commands[category]
                    print(f'Category "{category}" is empty and deleted.')

                self.save()

    def list_commands(self, category: str = None):
        if not self.commands:
            print(Fore.RED + "No commands stored.")
            return

        if category:
            if category in self.commands:
                # Color the category name header
                print(Fore.YELLOW + f"Commands in Category: {category}\n")

                longest_name = max(len(name)
                                   for name in self.commands[category])

                # Print headers with bold and aligned
                print(Fore.CYAN + Style.BRIGHT +
                      f'{"Command Name".ljust(longest_name + 20)}| Shell Command')
                print(Fore.CYAN + Style.BRIGHT +
                      f'{"-" * (longest_name + 20)}+{"-" * 50}')

                for name, cmd in self.commands[category].items():
                    # Print each command name in bright white, and the command in green
                    print(
                        Fore.GREEN + f'{name.ljust(longest_name + 20)}| ' + Fore.WHITE + Style.BRIGHT + cmd)

            else:
                print(Fore.RED + f'Category "{category}" not found.')
        else:
            print(Fore.YELLOW + "\nStored Commands by Category:")

            # Iterate over all categories and print the commands in the same format
            for cat, cmds in self.commands.items():
                longest_name = max(len(name) for name in cmds)

                # Print category header
                print(Fore.YELLOW + f"\nCommands in Category: {cat}\n")
                print(Fore.CYAN + Style.BRIGHT +
                      f'{"Command Name".ljust(longest_name + 20)}| Shell Command')
                print(Fore.CYAN + Style.BRIGHT +
                      f'{"-" * (longest_name + 20)}+{"-" * 50}')

                for name, cmd in cmds.items():
                    # Print command name in green and command in bright white
                    print(
                        Fore.GREEN + f'{name.ljust(longest_name + 20)}| ' + Fore.WHITE + Style.BRIGHT + cmd)

        print("\n\n\n")
