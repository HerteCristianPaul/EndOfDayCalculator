from termcolor import colored


class PyDataHandler:
    def deep_work_input(self, data):
        total_deep_work = 0
        for task in data['tasks']:
            if task['is_deep_work']:
                while True:
                    percentage_input = input(
                        colored(f"What % did you concentrate on task {task['task_name']} (int): ", "blue"))

                    try:
                        percentage = int(percentage_input)
                        break
                    except ValueError:
                        print(colored("Invalid input. Please enter a valid number.", "red"))

                task['deep_work'] = self.deep_work_calculator(percentage, task['task_time'])
                total_deep_work += self.deep_work_minutes(task['deep_work'])

        data['general_info']['total_deep_work'] = self.datetime(total_deep_work)

        return data

    def deep_work_calculator(self, percentage, total_time):
        hours, minutes, seconds = map(int, total_time.split(':'))
        total_minutes = (hours * 60) + minutes + (seconds / 60)
        deep_work = (percentage / 100) * total_minutes
        deep_work_hours = int(deep_work // 60)
        deep_work_minutes = int(deep_work % 60)

        return f'{deep_work_hours}:{deep_work_minutes}'

    def deep_work_minutes(self, time):
        hours, minutes = map(int, time.split(':'))
        total_minutes = (hours * 60) + minutes

        return total_minutes

    def datetime(self, minutes):
        deep_work_hours = int(minutes // 60)
        deep_work_minutes = int(minutes % 60)

        return f'{deep_work_hours}:{deep_work_minutes}'

    def completion_input(self, data):
        for task in data['tasks']:
            while True:
                task_status_input = input(
                    colored(f"Did you complete {task['task_name']} (y, n): ", "blue"))

                if task_status_input.lower() == 'y':
                    task['status'] = 'Done'
                    break
                elif task_status_input.lower() == 'n':
                    task['status'] = 'Unfinished'
                    break

        return data

    def process_data(self, data):
        total_value = 0
        done_value = 0
        for task in data['tasks']:
            if task['task_difficulty'] == 'Easy':
                total_value += 1
                if task['status'] == 'Done':
                    done_value += 1
            elif task['task_difficulty'] == 'Medium':
                total_value += 2
                if task['status'] == 'Done':
                    done_value += 2
            elif task['task_difficulty'] == 'Hard':
                total_value += 3
                if task['status'] == 'Done':
                    done_value += 3

        data['general_info']['completion'] = (done_value / total_value) * 100

        return data
