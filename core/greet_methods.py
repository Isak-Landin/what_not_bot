import time
from help_scripts import selenium_operator as sop
from core import initiate_control_port as selenium_override
import traceback


class Reading:
    def __init__(self):
        self.already_greeted = []
        self.to_be_greeted = []
        self.driver = selenium_override.initiate_driver()
        self.chat_element = self.get_chat_element()

        self.last_message_sent_time = None

    def return_chat_element(self):
        if self.chat_element is None:
            exit('Chat_element was none when trying to return from greet_methods')
        else:
            return self.chat_element

    def return_driver(self):
        if self.driver is None:
            exit('Driver was none when trying to return from greet_methods')
        else:
            return self.driver

    def get_chat_element(self):
        try:
            chat_element, succeeded = sop.find_object_XPATH(
                driver=self.driver,
                time_to_wait=3,
                _xpath='//*[@id="app"]/div[1]/div[2]/div[3]/div/div[1]',
            )

            if succeeded is False:
                chat_element, succeeded = sop.find_object_XPATH(
                    driver=self.driver,
                    time_to_wait=2,
                    _xpath='/html/body/div[1]/div[1]/div[2]/div[3]/div/div[1]'
                )

                if succeeded is False:
                    chat_element, succeeded = sop.find_object_XPATH(
                        driver=self.driver,
                        time_to_wait=2,
                        _xpath='//*[@id="app"]/div[1]/div[2]/div[4]/div/div[1]'
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
            print('Waiting to be greeted: ', to_greet)
            try:
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
                        if name not in to_greet and name not in not_to_greet:
                            to_greet.append(name)
            except:
                print(traceback.print_exc())