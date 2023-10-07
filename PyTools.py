from dotenv import load_dotenv
from chromedriver_py import binary_path
from selenium import webdriver
import os

load_dotenv()


class PyTools:
    def get_credentials(self):
        return {
            'username': os.getenv("LOGIN_EMAIL"),
            'password': os.getenv("LOGIN_PASSWORD"),
            'url': "https://clockify.me"
        }

    def get_driver(self):
        svc = self.google_driver_init()
        return webdriver.Chrome(service=svc)

    def google_driver_init(self):
        return webdriver.ChromeService(executable_path=binary_path)
