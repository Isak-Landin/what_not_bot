try:
    import traceback
    from help_scripts import executing_chrome
    import time

    executing_chrome.remove_all_existing_instances()
    executing_chrome.start_chrome(8001)

except:
    print(traceback.print_exc())
    time.sleep(10000)