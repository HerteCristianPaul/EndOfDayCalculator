import os
import glob
import csv
import questionary
from termcolor import colored


class PyExport:

    def export_file_type(self):
        file_type = questionary.select(
            "What do you want to calculate?",
            choices=[
                "CSV",
                "Excel (under construction)"
            ]).ask()

        return file_type

    def export_file_location(self):
        location = input(
            colored("Export location (leave blank if file location is in project root): ", "blue"))

        return location

    def export_files(self, file_type, directory_path="default"):
        if directory_path == "default":
            directory_path = os.getcwd()

        files = []
        if file_type == 'CSV':
            csv_files = glob.glob(os.path.join(directory_path, '*.csv'))
            if not csv_files:
                print(colored("No CSV files found in the directory.", "red"))
            else:
                for i, file in enumerate(csv_files):
                    files.append(os.path.basename(file))

        return files

    def export_select(self, files):
        chosen_file = questionary.select(
            "What do you want to calculate?",
            choices=files
        ).ask()

        return chosen_file

    def export_process(self, chosen_file):
        with open(chosen_file, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)

            data_list = []

            for row in csvreader:
                data_dict = {}
                for i in range(len(header)):
                    data_dict[header[i]] = row[i]

                data_list.append(data_dict)

        return data_list

    def convert_duration(self, data):
        for i, element in enumerate(data):
            time_parts = element['Duration (h)'].split(':')
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            minutes = minutes + (hours * 60)
            data[i]['Duration (h)'] = minutes

        return data

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

        return combined_data_list

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
                    except ValueError:
                        print(colored("Invalid input. Please enter a valid number.", "red"))

        return data

    def export_perc_calc(self, data):
        for element in data:
            tags = element['Tags']
            if 'DeepWork' in tags:
                element['DeepWork'] = int((float(element['Duration (perc)']) / 100) * element['Duration (h)'])

        return data

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

        return to_return

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
