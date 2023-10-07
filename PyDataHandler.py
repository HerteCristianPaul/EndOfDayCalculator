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
