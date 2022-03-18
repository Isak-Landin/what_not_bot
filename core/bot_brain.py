from help_scripts import bot_actions, general_actions
import ctypes
import multiprocessing
from pathlib import Path


user32 = ctypes.windll.user32
region = (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

print(Path().resolve())


def find_all_flowers(image):
    farm_region = (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

    def check_for_duplicates(generator_of_regions, name):
        completed_list = []
        refined_completed_list = [name]
        list_of_regions = list(generator_of_regions)

        if len(list_of_regions) > 1:
            for current_region in list_of_regions:
                completed_list.append(current_region)
                x_value_current_region = int(current_region[0])
                y_value_current_region = int(current_region[1])

                for other_region in list_of_regions:
                    print(name)
                    list_for_other_region = other_region

                    x_value_other_region = int(list_for_other_region[0])
                    y_value_other_region = int(list_for_other_region[1])

                    y_difference = y_value_other_region - y_value_current_region
                    x_difference = x_value_other_region - x_value_current_region
                    print((10 >= y_difference >= - 10 or y_difference == 0) and (10 >= x_difference >= -10 or x_difference == 0))
                    if (10 >= y_difference >= - 10 or y_difference == 0) and (10 >= x_difference >= -10 or x_difference == 0):
                        while other_region in list_of_regions:
                            list_of_regions.remove(other_region)
                            print('POPPED: ', other_region)

                if len(completed_list) > 1:
                    for completed_region in completed_list:
                        refined_region_current = completed_list.pop(completed_list.index(completed_region))
                        refined_completed_list.append(refined_region_current)

                        x_value_current_region = int(completed_region[0])
                        y_value_current_region = int(completed_region[1])
                        for other_completed_region in completed_list:
                            x_value_other_region = int(other_completed_region[0])
                            y_value_other_region = int(other_completed_region[1])

                            y_difference = y_value_current_region - y_value_other_region
                            x_difference = x_value_current_region - x_value_other_region

                            if (10 >= y_difference >= - 10 or y_difference == 0) and (
                                    10 >= x_difference >= -10 or x_difference == 0):
                                completed_list.remove(other_completed_region)

        return refined_completed_list

    all_of_type_image = bot_actions.VisualActions.find_images(
        image=str(Path().resolve()) + fr'\images\{image}',
        region=farm_region,
        confidence=0.6
    )

    completed_check = check_for_duplicates(all_of_type_image, name=image)

    return list(completed_check)