import time
import json
from help_scripts import selenium_operator as sop
from pathlib import Path
import traceback
from sys import exit

class Commands:
    def __init__(self, chat_element, driver):
        self.path_main = str(Path().resolve())
        self.driver = driver
        self.chat_element = chat_element

        self.commands_full_data = self.get_commands_from_storage()
        self.commands_keys = []
        self.get_keys_from_full_command_data()

        self.commands_to_execute = []
        self.commands_already_executed = []
        self.user_specific_command_request = []

        self.cooldown = time.time()

    def get_commands_from_storage(self):
        with open(fr'{self.path_main}\core\commands.json', 'r+') as file:
            commands_full_data = json.load(file)

        commands_full_data = commands_full_data['commands']

        # print('Commands_full_data', commands_full_data)

        return commands_full_data

    def get_keys_from_full_command_data(self):

        # Thought process #

        # Due to this commands collection only taking place once, a reference to the list
        # which will in the end be self.commands will not be needed in terms of a threading args
        # Rather this function will only be responsibly for getting the commands once at the start
        # of the script

        for key in self.commands_full_data:
            self.commands_keys.append(key)

    def look_for_commands_in_chat(self, commands_to_execute, commands_already_executed):
        while True:
            command = None
            name = None
            all_usernames_and_commands_div = None
            name_command_list_index = None
            try:
                all_usernames_and_commands_div, succeeded = sop.find_child_XPATH(
                    parent_object=self.chat_element,
                    _xpath='./div[1]'
                )

                if succeeded is False or all_usernames_and_commands_div is None:
                    exit('Could not find the all_usernames_and_commands')
            except:
                print('Failed to find all_usernames_and_commands_div')

            users_specific_commands, succeeded = sop.find_children_XPATH(
                parent_object=all_usernames_and_commands_div,
                _xpath='./div'
            )

            for user_cmd in users_specific_commands[-6:-1]:
                try:
                    user_with_image, succeeded = sop.find_child_XPATH(
                        parent_object=user_cmd,
                        _xpath='./img'
                    )

                    username_with_image_name, succeeded = sop.find_child_XPATH(
                        parent_object=user_cmd,
                        _xpath='./div[1]/span[1]'
                    )

                    username_with_image_cmd, succeeded = sop.find_child_XPATH(
                        parent_object=user_cmd,
                        _xpath='./div[1]/span[2]'
                    )

                    try:
                        name = username_with_image_name.text
                    except:
                        pass
                    try:
                        command = username_with_image_cmd.text
                    except:
                        pass

                finally:

                    if succeeded is False:

                        try:
                            user_with_no_image, succeeded = sop.find_child_XPATH(
                                parent_object=user_cmd,
                                _xpath='./div[2]'
                            )

                            username_with_no_image_name, succeeded = sop.find_child_XPATH(
                                parent_object=user_cmd,
                                _xpath='./div[2]/span[1]'
                            )

                            username_with_no_image_cmd, succeeded = sop.find_child_XPATH(
                                parent_object=user_cmd,
                                _xpath='./div[2]/span[2]'
                            )
                            try:
                                name = username_with_no_image_name.text
                            except:
                                print('FAILED!!!')
                            try:
                                command = username_with_no_image_cmd.text
                            except:
                                print('FAILED!!!')

                        except:
                            print('Failed to find both types of users')

                if name is None or name == 'Chat paused due to scroll' or name == ''\
                        or command is None:
                    print('Command or something else was None or invalid')
                    pass

                else:
                    print(name, command)
                    if command in self.commands_keys:
                        print('Putting together command and name')
                        try:
                            name = name.split(':')
                            name = name[0]

                            print('Name after removal of semicolon ', name)

                            name_command_list_index = [name, command, users_specific_commands.index(user_cmd)]
                        except:
                            pass

                        if name_command_list_index not in commands_to_execute\
                                and name_command_list_index:
                            print('Adding command to list', name_command_list_index)
                            commands_to_execute.append(name_command_list_index)
                            commands_already_executed.append(name_command_list_index[2])
                            print('index for command in list of messages: ', name_command_list_index[2])
                    else:
                        pass