import os
import inquirer
from .command_store import CommandStore
from colorama import Fore, Style, init

# Initialize colorama for colors
init(autoreset=True)

# Initialize the command store
store = CommandStore()
store.load()


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def interactive_mode():
    """Interactive mode for managing shell commands."""
    while True:
        # Clear the screen before displaying the menu
        clear_screen()

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
                inquirer.Text(
                    'name', message="Enter description for the command")
            ])['name']
            commands = inquirer.prompt([
                inquirer.Text(
                    'commands', message="Enter the shell command(s), separated by '&&'")
            ])['commands'].split("&&")

            store.add_command(
                category, name, [cmd.strip() for cmd in commands])
            print(Fore.GREEN + f'Command "{name}" added successfully.')

        elif action['action'] == 'Delete command':
            if not store.commands:
                print(Fore.RED + "No commands stored.")
                continue

            command_choices = {
                entry.description: entry for entry in store.commands}
            delete_question = [
                inquirer.List(
                    'name',
                    message="Choose a command to delete",
                    choices=list(command_choices.keys())
                )
            ]
            name = inquirer.prompt(delete_question)['name']

            store.delete_command(name)
            print(Fore.GREEN + f'Command "{name}" deleted successfully.')

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
                print(Fore.RED + "All commands deleted.")

        elif action['action'] == 'Exit':
            print(Fore.YELLOW + "Exiting interactive mode.")
            break

        # Wait for the user to press enter before clearing the screen and showing the menu again
        input(Fore.CYAN + "\nPress Enter to continue...")


def main():
    interactive_mode()


if __name__ == "__main__":
    main()
