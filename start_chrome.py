import traceback
from help_scripts import executing_chrome
import time


def start_chrome_base():
    try:
        is_successful_delete = executing_chrome.remove_all_existing_instances()
        is_successful_start = executing_chrome.start_chrome(8001)
        if is_successful_start is not False and is_successful_delete is not False:
            return True
        else:
            return False
    except:
        print(traceback.print_exc())
        return False
