from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


def initiate_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8001")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    return driver
