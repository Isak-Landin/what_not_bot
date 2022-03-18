from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pathlib
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback


def driver_get(driver, url):
    driver.get(url)


def find_object_XPATH(driver, time_to_wait, _xpath):
    object_to_find = None
    success = False
    try:
        object_to_find = WebDriverWait(driver, time_to_wait).until(EC.presence_of_element_located(
            (By.XPATH, _xpath)))
        success = True
    except:
        print('Could not find the object', _xpath)
        print(traceback.print_exc())
    finally:
        return object_to_find, success


def find_objects_XPATH(driver, time_to_wait, _xpath):
    objects_to_find = None
    success = False
    try:
        objects_to_find = WebDriverWait(driver, time_to_wait).until(EC.presence_of_all_elements_located(
            (By.XPATH, _xpath)))
        success = True
    except:
        print('Could not find the object', _xpath)
    finally:
        return objects_to_find, success


def find_children_XPATH(parent_object, _xpath, to_print=False):
    children = None
    success = False
    try:
        children = parent_object.find_elements(By.XPATH, _xpath)
        success = True
    except:
        if to_print:
            print('Could not find the child-objects for: ', _xpath)
    finally:
        return children, success


def find_child_XPATH(parent_object, _xpath, to_print=False):
    child = None
    success = False
    try:
        child = parent_object.find_element(By.XPATH, _xpath)
        success = True
    except:
        if to_print:
            print('Could not find the child-objects for: ', _xpath)
    finally:
        return child, success


def find_object_ID(driver, time_to_wait, _id):
    object_to_find = None
    success = False
    try:
        object_to_find = WebDriverWait(driver, time_to_wait).until(EC.presence_of_element_located(
            (By.ID, _id)))
        success = True
    except:
        print('Could not find the object', _id)
    finally:
        return object_to_find, success


def find_object_CLASS(driver, time_to_wait, _class):
    object_to_find = None
    success = False
    try:
        object_to_find = WebDriverWait(driver, time_to_wait).until(EC.presence_of_element_located(
            (By.ID, _class)))
        success = True
    except:
        print('Could not find the object', _class)
    finally:
        return object_to_find, success


def click_object(object_to_click):
    try_again = True
    try:
        object_to_click.click()
        try_again = False
    except:
        print(traceback.print_exc())
    finally:
        return try_again









