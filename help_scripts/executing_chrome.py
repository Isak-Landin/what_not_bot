import os
import pathlib
import shutil
import time
import traceback
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from sys import exit

path = str(pathlib.Path(__file__).parent.resolve())
path_to_chrome_instances = path + r'\instances_of_chrome'


def remove_all_existing_instances():
    all_instances = os.listdir(path_to_chrome_instances)

    if len(all_instances) != 0:
        for file in all_instances:
            try:
                os.remove(path=path_to_chrome_instances + '\\' + str(file))
            except:
                try:
                    shutil.rmtree(path_to_chrome_instances + '\\' + str(file))

                except:
                    print(traceback.print_exc())
                    return False


def start_chrome(port):
    driver = None
    try:
        command = fr'start chrome.exe --remote-debugging-port={port} --user-data-dir={path}' \
                  + r'\instances_of_chrome' + fr'\{port}'
        print('Creating directory')
        new_directory = path_to_chrome_instances + fr'\{port}'

        os.mkdir(new_directory)
        os.system(command)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        
        print(fr'{path}\chromedriver\chromedriver.exe')

        driver = webdriver.Chrome(executable_path=fr'{path}\chromedriver\chromedriver.exe',
                                  chrome_options=chrome_options)

    except:
        print(traceback.print_exc())
        return False

    finally:
        if driver is not None:
            return driver



