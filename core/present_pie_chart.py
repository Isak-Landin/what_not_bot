import pandas as pd
import matplotlib.pyplot as plt
import cv2 as parent_cv2
import cv2.cv2 as cv2
import time
import traceback
from pathlib import Path

"""class PresentPieChart:
    def __init__(self, labels=0, sizes_of_alternatives_in_list=0):
        self.data_sizes = sizes_of_alternatives_in_list
        self.labels = labels

        #####
        # For testing purposes the data will be fabricated and static
        self.labels = ['Alt1', 'Alt2', 'Alt3', 'Alt4']
        self.data_sizes = [10, 20, 30, 40]

        #####
        # Explode can be added to clarify the winner i.e:
        # explode = (0, 0.1, 0, 0)

    def building_pie_chart(self):
        def presenting_pie_chart(pie_chart_to_show):
            pie_chart_to_show.show()
        fig1, ax1 = plt.subplots()

        ax1.pie(self.data_sizes, labels=self.labels, autopct='%1.1f%%', startangle=0)
        ax1.axis('equal')

        presenting_pie_chart(plt)"""


def building_pie_chart(data_sizes, labels):
    def presenting_pie_chart(pie_chart_to_show):
        pie_chart_to_show.savefig('pie_chart.png')
        file = str(Path().resolve()) + r'\pie_chart.png'
        try:
            time.sleep(4)
            image = cv2.imread(file)
        except:
            print('Except reached')
            try:
                time.sleep(5)
                image = cv2.imread(file)
            except:
                print(traceback.print_exc())
                return

        to_continue = True

        cv2.imshow("Results", image)
        cv2.waitKey(0)

    try:
        fig1, ax1 = plt.subplots()

        ax1.pie(data_sizes, labels=labels, autopct='%1.1f%%', startangle=0)
        ax1.axis('equal')

        presenting_pie_chart(plt)
    except:
        print('This was your sizes: ', data_sizes)
        print('This was your labels: ', labels)