# Copyright (c) 2018 Mx (Shift Project delegate / 4446910057799968777S)
# Licensed under MIT License <see LICENSE file>

import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from data import config

options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')

# number_of_delegates = config.active_delegates


def DelegatesRedAndOrange(url, max_attempts, options=options):
    """
    Getts a data from Explorer's Delegate Monitor page.
    Using Selenium Web Browser Automation tool.
    This function starts a Chrome browser in headless mode.
    Then waits until delegates_table table loaded,
    then it checks is there any 'Missed block' or 'Not forging' delegates,
    if not, functions stops.
    If delegates table has one or more delegates with statuses
    'Not forging' anf 'Missed block' function saves data only with
    delegates with those statuses.

    Example of output:

    {
        1: {
            'NextTurn': '41 min 33 sec',
            'lastBlockTime': '2 days ago',
            'Name': 'kidnapped',
            'Status': 'Not forging'
        },
        5: {
            'NextTurn': '27 sec',
            'lastBlockTime': 'an hour ago',
            'Name': 'lol',
            'Status': 'Missed block'
        }
    }

    This function don't work with Firefox browser, because
    in gecodriver an action 'move_to_element' don't scroll the page.
    """

    delegates_table = {}
    attempt = 0

    for i in range(max_attempts):
        try:
            # For Windows
            # driver = webdriver.Chrome(chrome_options=options)

            # For Linux
            driver = webdriver.Chrome(
                chrome_options=options,
                executable_path=r'/usr/local/bin/chromedriver'
            )

            actions = ActionChains(driver)
            driver.get(url)
            wait = WebDriverWait(driver, 10)

            green_circle = 'i.green'
            red_circle = 'i.red'
            orange_circle = 'i.orange'

            # Waiting until a delegates table will be definitely loaded
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, green_circle))
            )
            """
            Waiting for explorer to be shure there all is okay
            Sometimes explorer shows delegates_table as "Missed block"
            or "Not forging" when it's not after fast loading.
            """
            time.sleep(3)

            missed_block_total_elem = driver.find_element_by_xpath(
                '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]/div'
                '/div/div/div[1]/div[1]/div[2]/div/p'
            ).get_attribute("innerHTML")

            not_forging_total_elem = driver.find_element_by_xpath(
                '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]/div'
                '/div/div/div[1]/div[1]/div[3]/div/p'
            ).get_attribute("innerHTML")

            zero_missed_block = int(missed_block_total_elem) == 0
            zero_not_forging = int(not_forging_total_elem) == 0

            if zero_missed_block and zero_not_forging:
                break

            circles_orange = (
                driver.find_elements_by_css_selector(orange_circle)
            )
            circles_red = (
                driver.find_elements_by_css_selector(red_circle)
            )

            def RankFromCircle(circles):
                rank = []

                for i in circles:
                    table_row = (
                        i
                        .find_element_by_xpath('..')
                        .find_element_by_xpath('..')
                    )
                    rank_elem = table_row.find_element_by_css_selector(
                        'td:nth-child(1)'
                    ).get_attribute("innerHTML")
                    rank.append(int(rank_elem))

                return rank

            red_and_orange = (
                RankFromCircle(circles_orange) + RankFromCircle(circles_red)
            )

            for i in red_and_orange:
                delegates_table[i] = {}

                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[2]/a'
                    .format(i)
                ).get_attribute("innerHTML")
                delegates_table[i]['Name'] = str(elem)

                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[5]'
                    .format(i)
                ).get_attribute("innerHTML")
                delegates_table[i]['NextTurn'] = str(elem)

                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[6]/i'
                    .format(i)
                ).get_attribute("outerHTML")

                forging = 'green' in str(elem)
                not_forging = 'red' in str(elem)
                missed_block = 'orange' in str(elem)

                if forging:
                    delegates_table[i]['Status'] = 'Forging'

                if not_forging:
                    delegates_table[i]['Status'] = 'Not forging'

                if missed_block:
                    delegates_table[i]['Status'] = 'Missed block'

                # Hovering over a circle to get status info visible
                element_to_hover_over = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]'
                    '/td[6]/i'.format(i)
                )
                actions.move_to_element(element_to_hover_over).perform()
                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[6]'
                    '/div/div[2]'.format(i)
                ).get_attribute("innerHTML")
                delegates_table[i]['lastBlockTime'] = (
                    str(elem).split('<br>')[2]
                )

                actions.reset_actions()
            break
        except Exception as ex:
            print('Error #{num}:'.format(num=attempt))
            print(ex)
            # Catching exeption when driver is not assigned
            try:
                driver.quit()
            except:
                pass
            attempt += 1
            pass
        finally:
            # Catching exeption when driver is not assigned
            try:
                driver.quit()
            except:
                pass

    return delegates_table


# def Delegates_table(url, max_attempts, options=options):
#     """
#     Getting a data from Explorer's Delegate Monitor page.
#     Using Selenium Web Browser Automation tool.
#     This function starts a Chrome browser in headless mode.
#     Then waits until delegates_table table loaded,
#     then it saves data from each delegates_table row.
#     Such data as 'Name', 'NextTurn', metadata from 'Circle'
#     and time of the last forged block from 'Status' column.
#     This function don't work with Firefox browser, because
#     in gecodriver an action 'move_to_element' don't scroll the page.
#     """

#     delegates_table = {}
#     attempt = 0

#     for i in range(max_attempts):
#         try:
#             # For Windows
#             # driver = webdriver.Chrome(chrome_options=options)

#             # For Linux
#             driver = webdriver.Chrome(
#                 chrome_options=options,
#                 executable_path=r'/usr/local/bin/chromedriver'
#             )

#             actions = ActionChains(driver)
#             driver.get(url)
#             wait = WebDriverWait(driver, 10)

#             # Waiting until a delegates table will be definitely loaded
#             wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "i.green"))
#             )
#             """
#             Waiting for explorer to be shure there all is okay
#             Sometimes explorer shows delegates_table as "Missed block"
#             or "Not forging" when it's not after fast loading.
#             """
#             time.sleep(3)

#             i = 1
#             while i <= number_of_delegates:
#                 delegates_table[i] = {}

#                 elem = driver.find_element_by_xpath(
#                     '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
#                     '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[2]/a'
#                     .format(i)
#                 ).get_attribute("innerHTML")
#                 delegates_table[i]['Name'] = str(elem)

#                 elem = driver.find_element_by_xpath(
#                     '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
#                     '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[5]'
#                     .format(i)
#                 ).get_attribute("innerHTML")
#                 delegates_table[i]['NextTurn'] = str(elem)

#                 elem = driver.find_element_by_xpath(
#                     '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
#                     '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[6]/i'
#                     .format(i)
#                 ).get_attribute("outerHTML")

#                 forging = 'green' in str(elem)
#                 not_forging = 'red' in str(elem)
#                 missed_block = 'orange' in str(elem)

#                 if forging:
#                     delegates_table[i]['Status'] = 'Forging'

#                 if not_forging:
#                     delegates_table[i]['Status'] = 'Not forging'

#                 if missed_block:
#                     delegates_table[i]['Status'] = 'Missed block'

#                 # Hovering over a circle to get status info visible
#                 element_to_hover_over = driver.find_element_by_xpath(
#                     '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
#                     '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]'
#                     '/td[6]/i'.format(i)
#                 )
#                 actions.move_to_element(element_to_hover_over).perform()
#                 elem = driver.find_element_by_xpath(
#                     '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
#                     '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[6]'
#                     '/div/div[2]'.format(i)
#                 ).get_attribute("innerHTML")
#                 delegates_table[i]['lastBlockTime'] = (
#                     str(elem).split('<br>')[2]
#                 )

#                 actions.reset_actions()
#                 i += 1
#             break
#         except Exception as ex:
#             print('Error #{num}:'.format(num=attempt))
#             print(ex)
#             # Catching exeption when driver is not assigned
#             try:
#                 driver.quit()
#             except:
#                 pass
#             attempt += 1
#             pass
#         finally:
#             # Catching exeption when driver is not assigned
#             try:
#                 driver.quit()
#             except:
#                 pass
#     return delegates_table
