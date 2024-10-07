import argparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import time


def main(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    # go to link
    driver.get(url)

    # expand buy ticket button
    expand_buy_ticket_element = WebDriverWait(driver, 600, 0.2).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/section[2]/div/div[1]/div/ul/li[1]/a"))
    )
    driver.execute_script("arguments[0].click();", expand_buy_ticket_element)

    # find ticket button
    robust_find_ticket_button_xpath = """
        /html/body/div[2]/div[1]/section[2]/div/div[2]/div[2]/table/tbody/tr/td[4]/button |
        /html/body/div[2]/div[1]/section[2]/div/div[2]/div[2]/table/tbody/tr[2]/td[4]/button
    """
    find_ticket_button = WebDriverWait(driver, 600, 0.2).until(
        EC.element_to_be_clickable((By.XPATH, robust_find_ticket_button_xpath))
    )
    driver.execute_script("arguments[0].click();", find_ticket_button)

    # select first available seat
    # make sure zone area list exists
    WebDriverWait(driver, 600, 0.2).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div/div[2]/div[2]"))
    )
    # Find all <a> elements within the zone area-list
    available_tickets_xpath = "//div[@class='zone area-list']//ul/li/a[font[@color='#FF0000']]"
    available_tickets = driver.find_elements(By.XPATH, available_tickets_xpath)
    if available_tickets:
        print("see available tickets")
        # Click the first available ticket
        first_available = available_tickets[0]
        driver.execute_script("arguments[0].click();", first_available)
    else:
        print("no available tickets")
        exit()

    # Select the maximum number of tickets available
    # Locate the select element
    select_element = WebDriverWait(driver, 600, 0.2).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div/form/div[1]/table/tbody/tr/td[2]/select"))
    )
    # Retrieve all option elements
    options = select_element.find_elements(By.TAG_NAME, "option")
    # Find the option with the maximum value
    max_value_option = max(options, key=lambda option: int(option.get_attribute("value")))
    # Click to select the option
    select_element.click()  # Open the dropdown
    max_value_option = WebDriverWait(driver, 600, 0.2).until(
        EC.element_to_be_clickable(max_value_option)
    )
    max_value_option.click()  # Select the largest option

    # TODO: verification code

    # agree term of service
    checkbox = WebDriverWait(driver, 600, 0.2).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div/form/div[3]/div/input"))
    )
    driver.execute_script("arguments[0].click();", checkbox)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, help="The url of the event")
    args = parser.parse_args()
    # TODO: target time
    target_time = datetime(2024, 10, 11, 12, 0, 0)
    # url = "https://tixcraft.com/activity/detail/24_yugyeom"
    # url = "https://tixcraft.com/activity/detail/24_tkl"
    # url = "https://tixcraft.com/activity/detail/24_dualipa"
    print("Waiting for the target time (2024-10-11 12:00:00)...")
    itr = 0
    log_interval = 5000
    while True:
        # Get the current time
        current_time = datetime.now()
        if itr % log_interval == (log_interval - 1):
            print("Still waiting...")
        # Check if the current time is greater than or equal to the target time
        if current_time >= target_time:
            start = datetime.now()
            main(args.url)
            end = datetime.now()
            print(start)
            print(end)
            print(end - start)
            break
        time.sleep(0.001)
        itr += 1
