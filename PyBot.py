from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from termcolor import colored
import sys


class PyBot:
    def __init__(self, login_credentials, driver):
        self.username = login_credentials['username']
        self.password = login_credentials['password']
        self.base_url = login_credentials['url']
        self.bot = driver

    def open_page(self):
        self.bot.get(self.base_url)

    def close_browser(self):
        self.bot.close()

    def login(self):
        login_page_button = self.bot.find_element(By.XPATH, '//*[@id="header"]/nav[1]/div/li/a')
        login_page_button.click()

        element_locator = (By.ID, "login-language-picker")
        wait = WebDriverWait(self.bot, 10)
        try:
            wait.until(EC.presence_of_element_located(element_locator))
        except TimeoutException:
            print(colored("Login Page - Element not found within the specified time", "red"))

        username_field = self.bot.find_element(By.ID, 'email')
        password_field = self.bot.find_element(By.ID, 'password')

        username_field.send_keys(self.username)
        password_field.send_keys(self.password)

        login_button = self.bot.find_element(By.XPATH, '/html/body/app-root/register-layout/div/div/div/div/div['
                                                       '2]/login/div/form/div/div/div/div[2]/div[5]/button')
        login_button.click()

        element_locator = (By.ID, "sidebar-menu")
        wait = WebDriverWait(self.bot, 10)
        try:
            wait.until(EC.presence_of_element_located(element_locator))
        except TimeoutException:
            print(colored("Home Page - Element not found within the specified time", "red"))

    def extract_intel(self):
        today = {
            'general_info': {},
            'tasks': []
        }
        today_entry_group = self.bot.find_element(By.XPATH, '//*[@id="layout-main"]/div/tracker2/div/div/div/div'
                                                            '/entry-group[1]')
        today_card = today_entry_group.find_element(By.CLASS_NAME, 'cl-card')
        today_header = today_card.find_element(By.CLASS_NAME, 'cl-card-header')
        child_div = today_header.find_elements(By.TAG_NAME, 'div')
        first_child_div = child_div[0]
        span_text = first_child_div.find_element(By.TAG_NAME, 'span').text

        if span_text != 'Today':
            print(colored("Today section isn't present", "red"))
            sys.exit()

        second_child_div = child_div[1]
        time_div = second_child_div.find_elements(By.TAG_NAME, 'div')
        total_time = time_div[1].text
        today['general_info']['total_time_today'] = total_time

        single_time_entries = today_card.find_elements(By.TAG_NAME, 'time-tracker-entry')
        parent_time_entries = today_card.find_elements(By.TAG_NAME, 'parent-tracker-entry')

        single_time_tasks = self.task_creation(single_time_entries, 'div/div[4]/div/div[1]/input-duration/input')
        parent_time_tasks = self.task_creation(parent_time_entries, 'div/div[4]/div/div[1]/div/input')

        today['tasks'] = single_time_tasks + parent_time_tasks

        return today

    def get_task_name(self, elem):
        return elem.find_element(By.XPATH, 'div/div[1]/span/div/input').get_attribute('title')

    def is_deep_work(self, elem):
        task_tags_span = elem.find_element(By.XPATH, 'div/div[3]/div/tag-names/div[2]/span')
        task_tags = task_tags_span.find_elements(By.CLASS_NAME, 'ng-star-inserted')
        for tag in task_tags:
            if tag.text.strip().replace(',', '') == 'DeepWork':
                return True
            else:
                return False

    def get_task_time(self, elem, route):
        return elem.find_element(By.XPATH, route).get_attribute('value')

    def task_creation(self, entries, timer_route):
        tasks = []
        for entry in entries:
            tasks.append({
                'task_name': self.get_task_name(entry),
                'is_deep_work': self.is_deep_work(entry),
                'task_time': self.get_task_time(entry, timer_route)
            })

        return tasks
