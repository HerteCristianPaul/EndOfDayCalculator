from termcolor import colored


class PyTarget:

    def percentage_input(self):
        task_dict = {
            'heavy_tasks_total': self.tasks_input('heavy', 'total'),
            'light_tasks_total': self.tasks_input('light', 'total'),
        }

        if task_dict['heavy_tasks_total'] == '':
            task_dict['heavy_tasks_done'] = ''
        else:
            task_dict['heavy_tasks_done'] = self.tasks_input('heavy', 'done')

        if task_dict['light_tasks_total'] == '':
            task_dict['light_tasks_done'] = ''
        else:
            task_dict['light_tasks_done'] = self.tasks_input('light', 'done')

        return task_dict

    def tasks_input(self, category, status):
        if status == 'total':
            part_question = 'tasks did you have'
        elif status == 'done':
            part_question = 'tasks did you complete'
        else:
            part_question = ''

        while True:
            input_tasks_total = input(
                colored(f"How many {category} {part_question}: ", "blue"))

            if input_tasks_total == '':
                return input_tasks_total

            try:
                tasks_total = float(input_tasks_total)
                return tasks_total
            except ValueError:
                print(colored("Invalid input. Please enter a valid number.", "red"))

    def percentage_calculate(self, task_dict):
        tasks_total = (2 * task_dict['heavy_tasks_total']) + task_dict['light_tasks_total']
        tasks_done = (2 * task_dict['heavy_tasks_done']) + task_dict['light_tasks_done']
        percentage_completion = (tasks_done / tasks_total) * 100

        print(colored(f"Target: {percentage_completion}%", "green"))
