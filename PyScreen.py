from termcolor import colored
import questionary
import sys

class py_screen:

    def __init__(self):
        print(colored('\n\nWelcome to EndOfDay Calculator\n', 'cyan', attrs=['bold']))
        self.choiose_category()

    def choiose_category(self):
        type = questionary.select(
            "What do you want to calculate?",
                choices=[
                    "Deep Work",
                    "Target Completion",
                ]).ask()

        self.category = 0 if type == 'Deep Work' else 1
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
            self.percentage_input()

    def deep_work_input(self):
        self.dp_inputs = []
        self.user_percentage = []

        while True:
            text = input(
                colored("How many tasks did you have (int): ", "blue"))

            try:
                number_of_tasks = int(text)
                break
            except ValueError:
                print(colored("Invalid input. Please enter a valid number.", "red"))

        for i in range(number_of_tasks):
            self.dp_inputs.append([])
            self.user_percentage.append([])
            while True:
                user_input = input(
                    colored(f"How many minutes did you spend on the deep work task {i} (int) (or blank to stop): ", "blue"))

                if user_input == "":
                    while True:
                        user_percentage = input(
                            colored(f"What % of concentration did you got on the task {i} (int): ", "blue"))

                        try:
                            self.user_percentage[i] = int(user_percentage)
                            break
                        except:
                            print(colored("Invalid input. Please enter a valid number.", "red"))

                    break

                try:
                    number = int(user_input)
                    self.dp_inputs[i].append(number)
                except ValueError:
                    print(colored("Invalid input. Please enter a valid number.", "red"))

        self.dp_calculate(number_of_tasks)

    def dp_calculate(self, number_of_tasks):
        total_minutes = 0
        for i in range(number_of_tasks):
            time_per_task = sum(self.dp_inputs[i])
            hours_per_task = time_per_task // 60
            minutes_per_task = time_per_task % 60
            result = time_per_task * self.user_percentage[i] / 100
            total_minutes = total_minutes + result
            print(colored(f"Task work{i}: {hours_per_task}h{minutes_per_task}m", "green"))

        hours = total_minutes // 60
        minutes = total_minutes % 60

        print(colored(f"Deep Work: {hours}h{minutes}m", "green"))
        self.close_continue()

    def percentage_input(self):
        task_dict = {
            'heavy_tasks_total': self.total_tasks('heavy'),
            'light_tasks_total': self.total_tasks('light'),
        }

        if task_dict['heavy_tasks_total'] == '':
            task_dict['heavy_tasks_done'] = ''
        else:
            task_dict['heavy_tasks_done'] = self.done_tasks('heavy')

        if task_dict['light_tasks_total'] == '':
            task_dict['light_tasks_done'] = ''
        else:
            task_dict['light_tasks_done'] = self.done_tasks('light')

        self.p_calculate(task_dict)

    def total_tasks(self, type):
        while True:
            input_tasks_total = input(
                colored(f"How many {type} tasks did you have: ", "blue"))

            if input_tasks_total == '':
                return input_tasks_total

            try:
                tasks_total = int(input_tasks_total)
                return tasks_total
            except:
                print(colored("Invalid input. Please enter a valid number.", "red"))

    def done_tasks(self, type):
        while True:
            input_tasks_done = input(
                colored(f"How many {type} tasks did you complete: ", "blue"))

            if input_tasks_done == '':
                return input_tasks_done

            try:
                tasks_done = int(input_tasks_done)
                return tasks_done
            except:
                print(colored("Invalid input. Please enter a valid number.", "red"))


    def p_calculate(self, task_dict):
        tasks_total = (2 * task_dict['heavy_tasks_total']) + task_dict['light_tasks_total']
        tasks_done = (2 * task_dict['heavy_tasks_done']) + task_dict['light_tasks_done']
        percentage_completion = (tasks_done / tasks_total) * 100

        print(colored(f"Target: {percentage_completion}%", "green"))
        self.close_continue()

    def close_continue(self):
        response = input(
            colored("Perform another calculation (n / y): ", "yellow"))

        if response == 'n':
            sys.exit()
        elif response == 'y':
            self.choiose_category()