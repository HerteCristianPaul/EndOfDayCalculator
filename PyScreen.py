from termcolor import colored
import questionary


class PyScreen:

    def __init__(self):
        print(colored('\n\nWelcome to EndOfDay Calculator\n', 'cyan', attrs=['bold']))

    def choice_category(self):
        choice = questionary.select(
            "What do you want to calculate?",
            choices=[
                "Scrape Intel",
                "Export",
                "Deep Work",
                "Target Completion"
            ]).ask()

        category = 0 if choice == 'Deep Work' \
            else 1 if choice == 'Target Completion' \
            else 2 if choice == 'Export' \
            else 3

        return category

    def display_title(self, chosen_category):
        if chosen_category == 0:
            print(colored('\n\nDeep Work Calculator\n', 'blue', attrs=['bold']))
        elif chosen_category == 1:
            print(colored('\n\nTarget Completion Calculator\n', 'blue', attrs=['bold']))
        elif chosen_category == 2:
            print(colored('\n\nExport Calculator\n', 'blue', attrs=['bold']))

    def display_intel(self, data):
        print(colored(f'Total time: {data["general_info"]["total_time_today"]}', 'magenta'))
        print(colored(f'Total DeepWork time: {data["general_info"]["total_deep_work"]}', 'magenta'))
        print(colored(f'Completion percentage: {data["general_info"]["completion"]}%', 'magenta'))
        for task in data['tasks']:
            print(colored(f'Task {task["task_name"]} took: {task["task_time"]}', 'blue'))
