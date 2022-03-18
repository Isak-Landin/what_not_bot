import threading
import subprocess
import multiprocessing
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from help_scripts import selenium_operator as sop
from selenium.webdriver.common.keys import Keys
import traceback
import time
import random
import json


class NotAName(Exception):
    pass


class Commands:
    def __init__(self, chat_element, driver):
        self.driver = driver
        self.chat_element = chat_element
        self.commands = []
        self.commands_to_execute = []
        self.user_specific_command_request = []
        self.cooldown = time.time()

    def get_commands_from_storage(self):
        with open('commands.json', 'r') as file:
            commands = json.load(file)

        commands = commands['commands']

        # Thought process #

        # Due to this commands collection only taking place once, a reference to the list
        # which will in the end be self.commands will not be needed in terms of a threading args
        # Rather this function will only be responsibly for getting the commands once at the start
        # of the script
        for key in commands:
            self.commands.append(key)

    def look_for_commands_in_chat(self, commands_to_execute):
        while True:
            pass


    def listen_for_commands(self):
        pass

    def answer_commands(self):
        pass


class Reading:
    def __init__(self):
        self.already_greeted = []
        self.to_be_greeted = []
        self.driver = None
        self.initiate_driver()
        self.chat_element = self.get_chat_element()

        self.last_message_sent_time = None

    def initiate_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8001")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def get_chat_element(self):
        try:
            chat_element, succeeded = sop.find_object_XPATH(
                driver=self.driver,
                time_to_wait=10,
                _xpath='//*[@id="app"]/div[1]/div[2]/div[3]/div/div[1]'
            )

            if succeeded is False:
                chat_element, succeeded = sop.find_object_XPATH(
                    driver=self.driver,
                    time_to_wait=5,
                    _xpath='/html/body/div[1]/div[1]/div[2]/div[3]/div/div[1]'
                )

            if succeeded is False:
                exit('Could not establish the chat window. The program is shutting down')

            return chat_element

        except:
            print('Could not establish the chat window. The program is shutting down')
            exit()

    def get_all_chat_messages(self, to_greet, not_to_greet):
        time.sleep(1)
        while True:
            try:
                print(self.to_be_greeted)
                all_usernames_and_messages = None
                all_usernames = []
                name = None
                try:

                    all_usernames_and_messages, succeeded = sop.find_child_XPATH(
                        parent_object=self.chat_element,
                        _xpath='./div[1]'
                    )

                    if succeeded is False:
                        exit('Could not find the all_usernames_and_messages')
                except:
                    pass

                users_specific_info, succeeded = sop.find_children_XPATH(
                    parent_object=all_usernames_and_messages,
                    _xpath='./div'
                )

                for user_info in users_specific_info[-5:]:
                    try:
                        user_with_image, succeeded = sop.find_child_XPATH(
                            parent_object=user_info,
                            _xpath='./img'
                        )

                        user_with_image_name, succeeded = sop.find_child_XPATH(
                            parent_object=user_info,
                            _xpath='./div[1]/span[1]'
                        )

                        name = user_with_image_name.text

                    except:
                        try:
                            user_with_no_image, succeeded = sop.find_child_XPATH(
                                parent_object=user_info,
                                _xpath='./div[2]'
                            )

                            name = user_with_no_image.text

                        except:
                            pass

                    if name is None or name == 'Chat paused due to scroll' or name == '':
                        pass

                    else:
                        try:
                            name = name.split(':')
                            name = name[0]
                        except:
                            pass
                        if name not in to_greet and name not in not_to_greet and name != "utbisalan":

                            to_greet.append(name)
            except:
                print(traceback.print_exc())

    def say_hello(self, to_greet, already_greeted_list, last_greeting_time):
        phrases = ["it's great seeing you here!", "what a pleasure seeing you here!",
                   "welcome to the stream of opportunity!"]
        chatbox, succeeded = sop.find_object_XPATH(
            driver = self.driver,
            time_to_wait=5,
            _xpath='//*[@id="app"]/div[1]/div[2]/div[3]/div/div[6]/div[1]/input'
        )
        
        if succeeded is False:
            chatbox, succeeded = sop.find_object_XPATH(
                driver=self.driver,
                time_to_wait=5,
                _xpath='/html/body/div[1]/div[1]/div[2]/div[3]/div/div[6]/div[1]/input'
            )

        if succeeded is False:
            exit('Could not find the chatbox, SHUTTING DOWN')
        while True:
            current_time = time.time()
            while current_time % last_greeting_time < 5:
                current_time = time.time()
                print(to_greet)
                print('Waiting 2')
                time.sleep(1)
            if len(to_greet) > 0:
                index_of_phrases = random.randint(0, (len(phrases) - 1))

                person_to_greet = to_greet.pop(0)
                if person_to_greet in to_greet:
                    to_greet.remove(person_to_greet)
                person_to_greet = f'Hello {person_to_greet}, {phrases[index_of_phrases]}'
                already_greeted_list.append(person_to_greet)

                chatbox.send_keys(person_to_greet)
                chatbox.send_keys(Keys.ENTER)
                last_greeting_time = time.time()



if __name__ == '__main__':
    reading_class = Reading()
    reading_class.last_message_sent_time = time.time()

    reading_chat_thread = threading.Thread(target=reading_class.get_all_chat_messages,
                                           args=[reading_class.to_be_greeted, reading_class.already_greeted])

    sending_messages_thread = threading.Thread(target=reading_class.say_hello,
                                               args=[reading_class.to_be_greeted, reading_class.already_greeted, reading_class.last_message_sent_time])
    reading_chat_thread.start()
    sending_messages_thread.start()

    print(reading_class.to_be_greeted)



