from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

path = str(Path(__file__).parent.resolve())

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:8001")
