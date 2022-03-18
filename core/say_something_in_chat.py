from help_scripts import selenium_operator as sop
import time
import random
import traceback
from selenium.webdriver.common.keys import Keys


def say_something(driver, to_greet, already_greeted_list, last_greeting_time,
                  commands_to_be_executed, last_command_time, command_all_data):
    phrases = ["it's great seeing you here!", "what a pleasure seeing you here!",
               "welcome to the stream of opportunity!", "days and nights pass and finally you are here"]
    succeeded = False
    chatbox = None
    try:
        chatbox, succeeded = sop.find_object_XPATH(
            driver=driver,
            time_to_wait=5,
            _xpath='//*[@id="app"]/div[1]/div[2]/div[3]/div/div[6]/div[1]/input'
        )

        if succeeded is False:
            chatbox, succeeded = sop.find_object_XPATH(
                driver=driver,
                time_to_wait=5,
                _xpath='/html/body/div[1]/div[1]/div[2]/div[3]/div/div[6]/div[1]/input'
            )
    except:
        print(traceback.print_exc())
        exit('Failed finding chatbox!!')

    if succeeded is False:
        exit('Could not find the chatbox, SHUTTING DOWN')
    while True:
        try:
            current_time = time.time()
            while current_time % last_greeting_time < 5 and current_time % last_command_time < 5:
                current_time = time.time()
                time.sleep(1)

            to_send_command = current_time % last_command_time > 5
            to_send_greeting = current_time % last_greeting_time > 5

            to_send_greeting = False

            # Temoporary false in place to only test commands
            # to_send_greeting = False
            if len(to_greet) > 0 and to_send_greeting is True:
                print('Trying to greet')
                try:
                    index_of_phrases = random.randint(0, (len(phrases) - 1))

                    person_to_greet = to_greet.pop(0)
                    if person_to_greet in to_greet:
                        to_greet.remove(person_to_greet)
                    person_to_greet = f'Hello {person_to_greet}, {phrases[index_of_phrases]}'
                    already_greeted_list.append(person_to_greet)

                    chatbox.send_keys(person_to_greet)
                    chatbox.send_keys(Keys.ENTER)
                    last_greeting_time = time.time()
                except:
                    print('Failed testing a greeting')

            if len(commands_to_be_executed) > 0 and to_send_command is True:
                print('Trying to command', commands_to_be_executed)
                try:
                    command_to_execute = commands_to_be_executed.pop(0)

                    if command_to_execute in commands_to_be_executed:
                        commands_to_be_executed.remove(command_to_execute)

                    response_name = command_to_execute[0]
                    response_command = command_all_data['commands'][command_to_execute[1]]

                    if 'NAME' in response_command:
                        response_command = response_command.replace('NAME', response_name)

                    chatbox.send_keys(response_command)
                    chatbox.send_keys(Keys.ENTER)
                    last_command_time = time.time()
                except:
                    print('Failed testing a command')

        except:
            print(traceback.print_exc())
            print('Failed to say something')
            continue
