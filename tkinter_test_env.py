from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont
import threading
from core import read_polling
from PIL import ImageTk, Image
from core import greet_methods as gm
from core import command_methods as cm
from core import say_something_in_chat as talk
import time
from sys import exit


class GUIWindow:
    def __init__(self, name_of_bot):
        self.name_of_bot = name_of_bot
        self.bot_core = StartAndStoreThreadData(name_of_bot=self.name_of_bot)
        self.list_of_alternative_entries = []
        self.timer_entry_widget = None

        self.root = Tk()
        self.root.title('What? Not-Bot')
        self.root.geometry("500x200")
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()
        self.label_poll = self.custom_label(text='Amount of alternatives: ').grid(column=0, row=0)
        self.entry_amount_of_entries = ttk.Entry(self.frame)
        self.entry_amount_of_entries.grid(column=1, row=0)
        self.button_poll = self.custom_button(
            text='Add entries',
            function_to_call=self.get_entry_times_to_dupe).grid(column=2, row=0)


        self.clear_entry_data = self.custom_button(text='Clear', function_to_call=self.clear_entry_data).grid(column=0, row=100)
        self.start_poll = self.custom_button(text='Start Poll', function_to_call=self.get_entry_data_then_start, width=20).grid(column=1, row=100)
        self.quit_button = self.custom_button(text='Quit', function_to_call=self.kill_all).grid(column=0, row=101)
        self.root.mainloop()

    def custom_button(self, text, function_to_call=None, width=15):
        button_to_return = ttk.Button(self.frame)
        if function_to_call is None:
            button_to_return = ttk.Button(self.frame, text=text, width=width)
        elif function_to_call is not None:
            button_to_return = ttk.Button(self.frame, text=text, command=function_to_call, width=width)

        return button_to_return

    def custom_label(self, text, font='Frank Ruhl Hofshi', size=12, weight='bold'):
        label_to_return = ttk.Label(self.frame, text=text)
        label_to_return.configure(font=(font, size, weight))
        return label_to_return

    def custom_entry(self):
        entry_to_return = ttk.Entry(self.frame)
        return entry_to_return

    def get_entry_times_to_dupe(self):
        if len(self.list_of_alternative_entries) > 0:
            self.timer_entry_widget.destroy()
            for entry in self.list_of_alternative_entries:
                entry.destroy()
        try:
            times = int(self.entry_amount_of_entries.get())
            if 1 > times > 7:
                raise ValueError
            else:
                print('Reached else statement')
                self.custom_entry_for_alternatives(times_to_dupe=times)

        except ValueError:
            print('Got a faulty value, try numbers instead. 1-7')

    def custom_entry_for_alternatives(self, times_to_dupe):
        self.root.geometry('500x350')

        for i in range(times_to_dupe):
            new_entry_to_grid = ttk.Entry(self.frame)
            new_entry_to_grid.insert(0, f'{i+1}')
            new_entry_to_grid.grid(column=0, row=i+1)

            self.list_of_alternative_entries.append(new_entry_to_grid)

        self.timer_entry_widget = ttk.Entry(self.frame)
        self.timer_entry_widget.insert(0, 'Timer (seconds)')
        self.timer_entry_widget.grid(column=0, row=times_to_dupe+2)

    def get_entry_data_then_start(self):
        list_of_alternatives = []
        timer = int(self.timer_entry_widget.get())
        for entry_object in self.list_of_alternative_entries:
            list_of_alternatives.append(entry_object)

    def clear_entry_data(self):
        self.root.geometry('500x200')
        for entry in self.list_of_alternative_entries:
            entry.destroy()

        self.timer_entry_widget.destroy()

    def kill_all(self):
        self.root.destroy()
        exit()



class Starting:
    def __init__(self):


        self.root = Tk()
        self.root.title('Starting the bot')
        self.root.geometry('300x150')
        self.frame = ttk.Frame(self.root)
        self.frame.grid()
        self.logo_load = ImageTk.PhotoImage(Image.open(r'images\rsz_robot.png'))
        self.logo_present = ttk.Label(self.frame, image=self.logo_load)
        self.logo_present.grid(column=0, row=0)
        self.name_of_bot_entry = ttk.Entry(self.frame)
        self.name_of_bot_entry.insert(0, 'Bot-account name')
        self.name_of_bot_entry.grid(column=0, row=1)
        self.button_to_start_bot = ttk.Button(self.frame, text='Start bot', command=self.start_polling_window)
        self.button_to_start_bot.grid(column=1, row=1)
        self.root.mainloop()

    def start_polling_window(self):
        name_of_bot = self.name_of_bot_entry.get()
        self.root.destroy()
        GUIWindow(name_of_bot=name_of_bot)


class StartAndStoreThreadData:
    def __init__(self, name_of_bot):
        self.reading_class = gm.Reading(name_of_bot=name_of_bot)
        self.reading_class.last_message_sent_time = time.time()
        self.commands_class = cm.Commands(chat_element=self.reading_class.get_chat_element(),
                                          driver=self.reading_class.return_driver())

        self.reading_chat_for_users_to_greet_thread = threading.Thread(target=self.reading_class.get_all_chat_messages,
                                                                  args=[self.reading_class.to_be_greeted,
                                                                        self.reading_class.already_greeted])

        self.reading_chat_for_commands = threading.Thread(
            target=self.commands_class.look_for_commands_in_chat,
            args=[self.commands_class.commands_to_execute, self.commands_class.commands_already_executed]
        )

        self.sending_messages_thread = threading.Thread(
            target=talk.say_something,
            args=[
                self.reading_class.return_driver(), self.reading_class.to_be_greeted,
                self.reading_class.already_greeted, self.reading_class.last_message_sent_time,
                self.commands_class.commands_to_execute, self.commands_class.cooldown,
                self.commands_class.commands_full_data])


        self.reading_chat_for_commands.daemon = True
        self.reading_chat_for_users_to_greet_thread.daemon = True
        self.sending_messages_thread.daemon = True

        self.reading_chat_for_commands.start()
        self.reading_chat_for_users_to_greet_thread.start()
        self.sending_messages_thread.start()

    def stop_threads(self):
        self.reading_chat_for_commands.join()
        self.reading_chat_for_users_to_greet_thread.join()
        self.sending_messages_thread.join()
        print('Quit all')



Starting()





