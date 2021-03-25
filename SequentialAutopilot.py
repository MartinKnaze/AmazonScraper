from SequentialScraper import master
from SequentialUpdater import create_data, identify_next_layer, data
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime

while True:
    # create_data()
    # identify_next_layer()
    try:
        master(data)
    except TimeoutException or WebDriverException:
        print("Exception handled at: ", datetime.now())
        pass

