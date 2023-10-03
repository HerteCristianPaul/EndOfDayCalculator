from termcolor import colored
import questionary
import sys
import os
import glob
import csv
from pprint import pprint

class py_screen:

    def __init__(self):
        print(colored('\n\nWelcome to EndOfDay Calculator\n', 'cyan', attrs=['bold']))
        self.choice_category()

    def choice_category(self):
        type = questionary.select(
            "What do you want to calculate?",
                choices=[
                    "Export",
                    "Deep Work",
                    "Target Completion"
                ]).ask()

        self.category = 0 if type == 'Deep Work' else 1 if type == 'Target Completion' else 2
        self.calculator_title()

    def calculator_title(self):
        if self.category == 0:
            print(colored('\n\nDeep Work Calculator\n', 'blue', attrs=['bold']))
        elif self.category == 1:
            print(colored('\n\nTarget Completion Calculator\n', 'blue', attrs=['bold']))
        elif self.category == 2:
            print(colored('\n\nExport Calculator\n', 'blue', attrs=['bold']))

        self.calculator_input()

    def calculator_input(self):
        if self.category == 0:
            self.deep_work_input()
        elif self.category == 1:
            self.percentage_input()
        elif self.category == 2:
            self.export_input()


    # DEEP WORK
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

    # TARGET COMPLETION
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
                tasks_total = float(input_tasks_total)
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
                tasks_done = float(input_tasks_done)
                return tasks_done
            except:
                print(colored("Invalid input. Please enter a valid number.", "red"))


    def p_calculate(self, task_dict):
        tasks_total = (2 * task_dict['heavy_tasks_total']) + task_dict['light_tasks_total']
        tasks_done = (2 * task_dict['heavy_tasks_done']) + task_dict['light_tasks_done']
        percentage_completion = (tasks_done / tasks_total) * 100

        print(colored(f"Target: {percentage_completion}%", "green"))
        self.close_continue()

    # EXPORT
    def export_input(self):
        file_type = questionary.select(
            "What do you want to calculate?",
            choices=[
                "CSV",
                "Excel (under construction)"
            ]).ask()

        location = input(
            colored("Export location (leave blank if file location is in project root): ", "blue"))

        if location == '':
            self.export_files(file_type)
        else:
            self.export_files(file_type, location)

    def export_files(self, file_type, directory_path="default"):
        if directory_path == "default":
            directory_path = os.getcwd()

        csv_files = glob.glob(os.path.join(directory_path, '*.csv'))
        if not csv_files:
            print(colored("No CSV files found in the directory.", "red"))
        else:
            files = []
            for i, file in enumerate(csv_files):
                files.append(os.path.basename(file))

        self.export_select(files)

    def export_select(self, files):
        chosen_file = questionary.select(
            "What do you want to calculate?",
            choices=files
            ).ask()

        self.export_process(chosen_file)

    def export_process(self, chosen_file):
        headers = []
        with open(chosen_file, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)

            data_list = []

            for row in csvreader:
                data_dict = {}
                for i in range(len(header)):
                    data_dict[header[i]] = row[i]

                data_list.append(data_dict)

        self.convert_duration(data_list)

    def convert_duration(self, data):
        for i, element in enumerate(data):
            time_parts = element['Duration (h)'].split(':')
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            minutes = minutes + (hours * 60)
            data[i]['Duration (h)'] = minutes

        self.task_creation(data)

    def task_creation(self, data):
        combined_entries = {}
        for entry in data:
            description = entry['Description']
            duration = float(entry['Duration (h)'])

            if description in combined_entries:
                combined_entries[description]['Duration (h)'] += duration
            else:
                combined_entries[description] = entry

        combined_data_list = list(combined_entries.values())

        self.task_perc_calc(combined_data_list)

    def task_perc_calc(self, data):
        for element in data:
            tags = element['Tags']

            if 'DeepWork' in tags:
                while True:
                    response = input(
                        colored(f"How concentrated were you on the task {element['Description']}(%): ", "blue"))

                    try:
                        perc = int(response)
                        element['Duration (perc)'] = perc
                        break
                    except:
                        print(colored("Invalid input. Please enter a valid number.", "red"))

        self.export_perc_calc(data)

    def export_perc_calc(self, data):
        for element in data:
            tags = element['Tags']
            if 'DeepWork' in tags:
                element['DeepWork'] = int((float(element['Duration (perc)']) / 100) * element['Duration (h)'])

        self.export_time_calc(data)

    def export_time_calc(self, data):
        total_time, deep_work = 0, 0
        for element in data:
            total_time += element['Duration (h)']
            tags = element['Tags']
            if 'DeepWork' in tags:
                deep_work += element['DeepWork']

        to_return = {
            'data': data,
            'total_time': total_time,
            'deep_work': deep_work
        }

        self.export_display(to_return)

    def export_display(self, data):
        for element in data['data']:
            hours = element['Duration (h)'] // 60
            minutes_left = int(element['Duration (h)'] % 60)
            print(colored(f"{element['Description']} took {hours}h {minutes_left}m", "magenta"))

        total_hours = data['total_time'] // 60
        total_minutes_left = int(data['total_time'] % 60)
        print(colored(f"Total Time: {total_hours}h {total_minutes_left}m", "magenta"))

        deep_hours = data['deep_work'] // 60
        deep_minutes_left = int(data['deep_work'] % 60)
        print(colored(f"DeepWork Time: {deep_hours}h {deep_minutes_left}m", "magenta"))

    def close_continue(self):
        response = input(
            colored("Perform another calculation (n / y): ", "yellow"))

        if response == 'n':
            sys.exit()
        elif response == 'y':
            self.choiose_category()