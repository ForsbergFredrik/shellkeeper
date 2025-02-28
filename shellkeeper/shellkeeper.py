#!/usr/bin/env python3

import argparse
from .command_store import CommandStore
import inquirer

# Initialize the command store
store = CommandStore()
store.load()


def interactive_mode():
    """Interactive mode for managing shell commands."""
    while True:
        # Prompt user with available options
        questions = [
            inquirer.List('action',
                          message="Choose an action",
                          choices=['List commands', 'Add command', 'Delete command',
                                   'Search command', 'Clear all commands', 'Exit'],
                          ),
        ]
        action = inquirer.prompt(questions)

        if action['action'] == 'List commands':
            category = inquirer.prompt([
                inquirer.Text(
                    'category', message="Enter category (leave blank for all)", default="")
            ])['category']
            store.list_commands(category if category else None)

        elif action['action'] == 'Add command':
            category = inquirer.prompt([
                inquirer.Text(
                    'category', message="Enter category for the command")
            ])['category']
            name = inquirer.prompt([
                inquirer.Text('name', message="Enter name for the command")
            ])['name']
            command = inquirer.prompt([
                inquirer.Text('command', message="Enter the shell command")
            ])['command']
            store.add_command(category, name, command)

        elif action['action'] == 'Delete command':
            name = inquirer.prompt([
                inquirer.Text(
                    'name', message="Enter the name of the command to delete")
            ])['name']
            store.delete_command(name)

        elif action['action'] == 'Search command':
            search_term = inquirer.prompt([
                inquirer.Text('search_term', message="Enter a search term")
            ])['search_term']
            store.search_command(search_term)

        elif action['action'] == 'Clear all commands':
            confirm = inquirer.prompt([
                inquirer.Confirm(
                    'confirm', message="Are you sure you want to delete all commands?", default=False)
            ])['confirm']
            if confirm:
                store.commands.clear()
                store.save()
                print("All commands deleted.")

        elif action['action'] == 'Exit':
            print("Exiting interactive mode.")
            break


def cli_menu():
    """Command-line interface for managing shell commands."""
    parser = argparse.ArgumentParser(
        description="Manage stored shell commands.")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    # List commands (optional category)
    list_parser = subparsers.add_parser(
        "list", help="List all stored commands")
    list_parser.add_argument("category", nargs="?",
                             default=None, help="Category to filter by")

    # Add command with category
    add_parser = subparsers.add_parser("add", help="Add a new command")
    add_parser.add_argument("category", help="Category of the command")
    add_parser.add_argument("name", help="Name of the command")
    add_parser.add_argument("shell_command", help="Shell command to execute")

    # Delete command with category
    delete_parser = subparsers.add_parser("delete", help="Delete a command")
    delete_parser.add_argument("name", help="Name of the command to delete")

    # Search commands
    search_parser = subparsers.add_parser(
        "search", help="Search for a command")
    search_parser.add_argument("search_term", help="Search term")

    # Clear all commands
    subparsers.add_parser("clear", help="Delete all stored commands")

    # Interactive mode
    subparsers.add_parser(
        "interactive", help="Run the CLI in interactive mode")

    args = parser.parse_args()

    # Command execution mapping
    commands = {
        "list": lambda: store.list_commands(args.category),
        "add": lambda: store.add_command(args.category, args.name, args.shell_command),
        "delete": lambda: store.delete_command(args.name),
        "search": lambda: store.search_command(args.search_term),
        "clear": lambda: store.commands.clear() or store.save() or print("All commands deleted."),
    }

    if args.command == "interactive":
        interactive_mode()
    else:
        if args.command:
            commands[args.command]()
        else:
            parser.print_help()

def main():
    cli_menu()

if __name__ == "__main__":
    main()
