
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
class CommandEntry:
    category: str
    description: str
    commands:  list[str] = field(default_factory=list)


@dataclass
class CommandEntry:
    category: str
    description: str
    commands:  list[str] = field(default_factory=list)

    def __str__(self):

        commands_str = f"{Fore.MAGENTA}- {Style.BRIGHT}{self.commands[0]}{Style.RESET_ALL}\n"
        for cmd in self.commands[1:]:
            commands_str += f"{"".ljust(20)}| {Fore.MAGENTA}- {Style.BRIGHT}{cmd}{Style.RESET_ALL}\n"
        # Create a formatted string for the Description and Commands
        formatted_string = (
            f"{Fore.YELLOW}{Style.BRIGHT}{'Description'.ljust(20)}| {'Commands':<30}{Style.RESET_ALL}\n"
            f"{'-' * 50}\n"
            f"{self.description.ljust(20)}| {commands_str}\n"
            f"{'-' * 50}"
        )

        return formatted_string


@dataclass
class CommandStore:
    commands: list[CommandEntry] = field(default_factory=list)

    def load(self):
        """Loads commands from the store file, handling empty or corrupt files."""
        if os.path.exists(store_file):
            try:
                with open(store_file, 'r') as file:
                    data = file.read().strip()

                    if not data:  # Handle empty file
                        print(Fore.YELLOW +
                              "Warning: store.json is empty. Starting fresh.")
                        self.commands = []
                        return

                    raw_entries = json.loads(data)
                    self.commands = [CommandEntry(**entry)
                                     for entry in raw_entries]

            except (json.JSONDecodeError, ValueError) as e:
                print(
                    Fore.RED + f"Error loading store.json: {e}. Resetting file.")
                self.commands = []
                self.save()  # Reset the file
        else:
            self.commands = []

    def save(self):
        with open(store_file, 'w') as file:
            json.dump([entry.__dict__ for entry in self.commands],
                      file, indent=4)

    def add_command(self, category: str, name: str, commands: str):
        print("Add command called", commands)
        command_entry = CommandEntry(
            category=category, description=name, commands=commands)
        self.commands.append(command_entry)
        self.save()

    def delete_command(self, name: str):
        for command in self.commands:
            if command.description == name:
                self.commands.remove(command)
                self.save()
                return
        print(f'Command "{name}" not found.')

    def list_commands(self, category: str = None):
        """Lists all commands, filtered by category if specified."""
        if not self.commands:
            print(Fore.RED + "No commands stored.")
            return

        if category:
            filtered_entries = [
                entry for entry in self.commands if entry.category.lower() == category.lower()]

            if not filtered_entries:
                print(Fore.RED + f'Category "{category}" not found.')
                return

            print(Fore.YELLOW + f"\nCommands in Category: {category}\n")
            for entry in filtered_entries:
                print(entry)

        else:
            print(Fore.YELLOW + "\nStored Commands by Category:\n")
            categorized_entries = {}

            # Group entries by category
            for entry in self.commands:
                categorized_entries.setdefault(
                    entry.category, []).append(entry)

            # Print each category with its commands
            for cat, entries in categorized_entries.items():
                print(f"{Style.RESET_ALL}{Fore.CYAN}[{cat}]\n\n")

                for entry in entries:
                    print(entry)  # Calls CommandEntry's __str__ method

            print("\n")
