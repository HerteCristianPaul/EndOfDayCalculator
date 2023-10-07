from PyScreen import PyScreen
from PyDeepWork import PyDeepWork
from PyTarget import PyTarget
from PyExport import PyExport
from PyTools import PyTools
from PyBot import PyBot
from PyDataHandler import PyDataHandler
import sys
from termcolor import colored
import pprint


def main():
    init()


def init():
    py_screen = PyScreen()
    chosen_category = py_screen.choice_category()
    py_screen.display_title(chosen_category)

    if chosen_category == 0:
        deep_work_calculator()
    elif chosen_category == 1:
        target_completion_calculator()
    elif chosen_category == 2:
        export_calculator()
    elif chosen_category == 3:
        scraper()


def close_continue():
    response = input(
        colored("Perform another calculation (n / y): ", "yellow"))

    if response == 'n':
        sys.exit()
    elif response == 'y':
        init()


def deep_work_calculator():
    py_deepwork = PyDeepWork()
    py_deepwork.deep_work_calculate()
    close_continue()


def target_completion_calculator():
    py_target = PyTarget()
    tasks = py_target.percentage_input()
    py_target.percentage_calculate(tasks)
    close_continue()


def export_calculator():
    py_export = PyExport()
    file_type = py_export.export_file_type()
    file_location = py_export.export_file_location()
    files = py_export.export_files(file_type, file_location)
    chosen_file = py_export.export_select(files)
    data_list = py_export.export_process(chosen_file)
    data = py_export.convert_duration(data_list)
    combined_data_list = py_export.task_creation(data)
    data2 = py_export.task_perc_calc(combined_data_list)
    data3 = py_export.export_perc_calc(data2)
    data4 = py_export.export_time_calc(data3)
    py_export.export_display(data4)
    close_continue()


def scraper():
    py_tools = PyTools()
    login_credentials = py_tools.get_credentials()
    driver = py_tools.get_driver()
    py_bot = PyBot(login_credentials, driver)
    py_bot.open_page()
    py_bot.login()
    data = py_bot.extract_intel()
    py_bot.close_browser()
    py_data_handler = PyDataHandler()
    intel = py_data_handler.deep_work_input(data)
    pprint.pprint(intel)
    py_screen = PyScreen()
    py_screen.display_intel(intel)


if __name__ == "__main__":
    main()
