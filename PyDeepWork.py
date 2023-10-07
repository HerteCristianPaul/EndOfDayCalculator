from termcolor import colored


class PyDeepWork:

    def __init__(self):
        self.dp_inputs = []
        self.user_percentage = []

        while True:
            text = input(
                colored("How many tasks did you have (int): ", "blue"))

            try:
                self.number_of_tasks = int(text)
                break
            except ValueError:
                print(colored("Invalid input. Please enter a valid number.", "red"))

        for i in range(self.number_of_tasks):
            self.dp_inputs.append([])
            self.user_percentage.append([])
            while True:
                user_input = input(
                    colored(f"How many minutes did you spend on the deep work task {i} (int) (or blank to stop): ",
                            "blue"))

                if user_input == "":
                    while True:
                        user_percentage = input(
                            colored(f"What % of concentration did you got on the task {i} (int): ", "blue"))

                        try:
                            self.user_percentage[i] = int(user_percentage)
                            break
                        except ValueError:
                            print(colored("Invalid input. Please enter a valid number.", "red"))
                    break

                try:
                    number = int(user_input)
                    self.dp_inputs[i].append(number)
                except ValueError:
                    print(colored("Invalid input. Please enter a valid number.", "red"))

    def deep_work_calculate(self):
        total_minutes = 0
        for i in range(self.number_of_tasks):
            time_per_task = sum(self.dp_inputs[i])
            hours_per_task = time_per_task // 60
            minutes_per_task = time_per_task % 60
            result = time_per_task * self.user_percentage[i] / 100
            total_minutes = total_minutes + result
            print(colored(f"Task work{i}: {hours_per_task}h{minutes_per_task}m", "green"))

        hours = total_minutes // 60
        minutes = total_minutes % 60

        print(colored(f"Deep Work: {hours}h{minutes}m", "green"))
