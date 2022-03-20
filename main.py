import threading
import time
from core import greet_methods as gm
from core import command_methods as cm
from core import say_something_in_chat as talk


class NotAName(Exception):
    pass


if __name__ == '__main__':

    reading_class = gm.Reading()
    reading_class.last_message_sent_time = time.time()

    commands_class = cm.Commands(chat_element=reading_class.get_chat_element(),
                                 driver=reading_class.return_driver())

    reading_chat_for_users_to_greet_thread = threading.Thread(target=reading_class.get_all_chat_messages,
                                                              args=[reading_class.to_be_greeted, reading_class.already_greeted])

    reading_chat_for_commands = threading.Thread(
        target=commands_class.look_for_commands_in_chat,
        args=[commands_class.commands_to_execute, 'random_place_holder']
    )
    driver = reading_class.return_driver()

    sending_messages_thread = threading.Thread(
        target=talk.say_something,
        args=[
            driver, reading_class.to_be_greeted,
            reading_class.already_greeted, reading_class.last_message_sent_time,
            commands_class.commands_to_execute, commands_class.cooldown,
            commands_class.commands_full_data])

    reading_chat_for_commands.start()
    reading_chat_for_users_to_greet_thread.start()
    sending_messages_thread.start()



