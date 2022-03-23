import json
import time
import pandas
from help_scripts import selenium_operator as sop
from core import present_pie_chart


class ReadingPollChat:
    def __init__(self, driver, chat_element):
        self.driver = driver
        self.user_data_is_collected = []
        self.alternatives = []
        self.data_sizes = []
        self.chat_element = chat_element

        self.timer = 0

    def clear_all_data(self):
        self.user_data_is_collected = []
        self.data_sizes = []
        self.timer = 0

    def visualize_data(self):
        pass

    def look_for_alternatives_in_chat(self, timer_object, vote_alternatives, data_size_list, already_voted):
        time_started = time.time()
        name = None
        vote_or_message = None
        for i in range(len(vote_alternatives)):
            data_size_list.append(0)
        while time.time() % time_started < timer_object:
            all_usernames_and_votes_div = None
            try:
                all_usernames_and_votes_div, succeeded = sop.find_child_XPATH(
                    parent_object=self.chat_element,
                    _xpath='./div[1]'
                )

                if succeeded is False or all_usernames_and_votes_div is None:
                    print('Failed initiating polls placeholder')
                    return 'Failed initiating poll placeholder'
            except:
                print('Failed to find all_usernames_and_commands_div')

            users_specific_votes, succeeded = sop.find_children_XPATH(
                parent_object=all_usernames_and_votes_div,
                _xpath='./div'
            )

            for vote in users_specific_votes[-7:-1]:
                try:
                    user_with_image, succeeded = sop.find_child_XPATH(
                        parent_object=vote,
                        _xpath='./img'
                    )

                    username_with_image_name, succeeded = sop.find_child_XPATH(
                        parent_object=vote,
                        _xpath='./div[1]/span[1]'
                    )

                    username_with_image_vote, succeeded = sop.find_child_XPATH(
                        parent_object=vote,
                        _xpath='./div[1]/span[2]'
                    )

                    try:
                        name = username_with_image_name.text
                    except:
                        pass
                    try:
                        vote_or_message = username_with_image_vote.text
                    except:
                        pass

                finally:

                    if succeeded is False:

                        try:
                            user_with_no_image, succeeded = sop.find_child_XPATH(
                                parent_object=vote,
                                _xpath='./div[2]'
                            )

                            username_with_no_image_name, succeeded = sop.find_child_XPATH(
                                parent_object=vote,
                                _xpath='./div[2]/span[1]'
                            )

                            username_with_no_image_cmd, succeeded = sop.find_child_XPATH(
                                parent_object=vote,
                                _xpath='./div[2]/span[2]'
                            )
                            try:
                                name = username_with_no_image_name.text
                            except:
                                print('FAILED!!!')
                            try:
                                vote_or_message = username_with_no_image_cmd.text
                            except:
                                print('FAILED!!!')

                        except:
                            print('Failed to find both types of users')
                    # Remove already voted for testing
                    if vote_or_message in vote_alternatives and name not in already_voted:
                        index_of_alternative = vote_alternatives.index(vote_or_message)
                        if len(vote_or_message) == len(vote_alternatives[index_of_alternative]):

                            data_size_list[index_of_alternative] += 1
                            already_voted.append(name)
                            print(already_voted)
                            print(vote_or_message)



        # Once this point is reached it indicates that the reading of chat for poll data has ended
        # Therefore call visualize_data_method
        present_pie_chart.building_pie_chart(data_size_list, vote_alternatives)


