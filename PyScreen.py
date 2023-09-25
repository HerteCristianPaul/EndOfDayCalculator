from termcolor import colored
import questionary
import sys

class py_screen:

    def __init__(self):
        print(colored('\n\nWelcome to EndOfDay Calculator\n', 'red', attrs=['bold']))
        self.choiose_category()

    def choiose_category(self):
        type = questionary.rawselect(
            "What do you want to calculate?",
                choices=[
                    "Deep Work",
                    "Target Completion",
                ]).ask()

        self.category = 0 if type == 0 else 1
        self.calculator_title()

    def calculator_title(self):
        if self.category == 0:
            print(colored('\n\nDeep Work Calculator\n', 'blue', attrs=['bold']))
        elif self.category == 1:
            print(colored('\n\nTarget Completion Calculator\n', 'blue', attrs=['bold']))

        self.calculator_input()

    def calculator_input(self):
        if self.category == 0:
            self.deep_work_input()
        elif self.category == 1:
            self.percentage()

    def deep_work_input(self):
        self.dp_inputs = []
        self.user_percentage = []

        number_of_tasks = input(
            colored("How many heavy tasks did you have: ", "cyan"))

        for i in range(number_of_tasks):
            while True:
                user_input = input(
                    colored("How many minutes did you spend on the deep work tasks (or blank to stop): ", "cyan"))

                if user_input == "":
                    self.user_percentage[i] = input(
                        colored("What % of concentration did you got on the current task: ", "cyan"))
                    break

                try:
                    number = int(user_input)
                    numbers.append(number)
                    self.dp_inputs[i].append(numbers)
                except ValueError:
                    print(colored("Invalid input. Please enter a valid number.", "red"))

        self.dp_calculate(number_of_tasks)

    def dp_calculate(self, number_of_tasks):
        total_minutes = 0
        for i in range(number_of_tasks):
            time_per_task = sum(self.dp_inputs[i])
            result = time_per_task * self.user_percentage[i] / 100
            total_minutes = total_minutes + result

        hours = total_minutes // 60
        minutes = total_minutes % 60

        print(colored("Deep Work: {hours}h{minutes}m", "red"))
        self.close_continue()

    def percentage_input(self):
        light_tasks_total = input(
            colored("How many light tasks did you have: ", "cyan"))

        heavy_tasks_total = input(
            colored("How many heavy tasks did you have: ", "cyan"))

        light_tasks_done = input(
            colored("How many light tasks did you complete: ", "cyan"))

        heavy_tasks_done = input(
            colored("How many heavy tasks did you complete: ", "cyan"))

        self.p_calculate(light_tasks_total, light_tasks_done, heavy_tasks_total, heavy_tasks_done)

    def p_calculate(self, light_tasks_total, light_tasks_done, heavy_tasks_total, heavy_tasks_done):
        light_tasks_remaining = light_tasks_total - light_tasks_done
        heavy_tasks_remaining = heavy_tasks_total - heavy_tasks_done

        tasks_total = heavy_tasks_total + (2 * light_tasks_total)
        tasks_remaining = heavy_tasks_remaining + (2 * light_tasks_remaining)
        tasks_done = heavy_tasks_done + (2 * light_tasks_done)

        percentage_completion = (tasks_done / tasks_total) * 100

        print(colored("Target: {percentage_completion}%", "red"))

    def close_continue(self):
        response = input(
            colored("Perform another calculation (n / y): ", "cyan"))

        if response == 'n':
            sys.exit()
        elif response == 'y':
            self.choiose_category()