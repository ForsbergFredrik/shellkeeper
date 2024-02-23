#!/usr/bin/env python3

import json
import argparse

COMMANDS_FILE = "/usr/local/share/shellkeeper_commands.json"
# COMMANDS_FILE = "shellkeeper_commands.json"

def load_commands():
    try:
        with open(COMMANDS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print('File not found')
        return None


def list_commands():
    commands = load_commands()
    print_commands(commands)

def search_command(search_term):
    all_commands = load_commands()
    filtered_commands = {name : command for name, command in all_commands.items() if search_term.lower() in name.lower() or search_term.lower() in command.lower()}
    print_commands(filtered_commands, f'Search results for "{search_term}"')

def print_commands(commands, title="Stored commands"):
    if commands:
        longest_name = max(len(name) for name in commands.keys())  # Find the longest command name for alignment
        print(f"\n{title}:\n")
        print(f'{"Command Name".ljust(longest_name + 4)}| Shell Command')
        print(f'{"-" * (longest_name + 4)}+{"-" * 15}')
        for name, command in commands.items():
            print(f'{name.ljust(longest_name + 4)}| {command}')
    else:
        print("No commands stored.")


def save_commands(commands):
    """Save commands to the storage file."""
    with open(COMMANDS_FILE, 'w') as file:
        json.dump(commands, file, indent=4)

def add_command(name, command):
    commands = load_commands()
    commands[name] = command
    save_commands(commands)
    print(f'Command "{name}" added successfully.')

def delete_command(name):
    commands = load_commands()
    del commands[name]
    save_commands(commands)
    print(f'Command "{name}" deleted successfully.')

def clear_all_commands():
    with open(COMMANDS_FILE, 'w') as file:
        json.dump({}, file)
        print("All commands deleted successfully.")

def main():
    parser = argparse.ArgumentParser(description="Manage stored shell commands.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add Commands
    add_parser = subparsers.add_parser("add", help="Add a new command")
    add_parser.add_argument("name", help="Name of the command")
    add_parser.add_argument("shell_command", help="Shell command to be executed (use '', Single quotes prevent the shell from interpreting the characters inside)")

    # Delete Commands
    delete_parser = subparsers.add_parser("delete", help="Delete a command")
    delete_parser.add_argument("name", help="Name of the command to delete")

    # List Commands
    list_parser = subparsers.add_parser("list", help="List all stored commands")

    # Search Commands
    search_parser = subparsers.add_parser("search", help="Search for a command")
    search_parser.add_argument("search_term", help="Search term")

    # Clear Commands
    clear_commands = subparsers.add_parser("clear", help="Delete all stored commands")


    args = parser.parse_args()

    if args.command == "add":
        add_command(args.name, args.shell_command)
    elif args.command == "delete":
        delete_command(args.name)
    elif args.command == "list":
        list_commands()
    elif args.command == "search":
        search_command(args.search_term)
    elif args.command == "clear":
        clear_all_commands()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()