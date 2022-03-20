from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from pathlib import Path


def initiate_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8001")
    driver = webdriver.Chrome(str(Path().resolve()) + r'\help_scripts\chromedriver\chromedriver.exe', options=chrome_options)

    return driver
