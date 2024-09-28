import argparse
import os
import base64

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import numpy as np
import time
from tqdm import tqdm


def random_encoding():
    seed = 42
    np.random.seed(seed)
    # generate a random encoding
    matrix = np.zeros((4, 26), dtype=int)
    for i in range(4):
        matrix[i, np.random.choice(26)] = 1
    return matrix


def encoding_to_text(encoding):
    # encoding: 4, 26
    indices = np.argmax(encoding, axis=1)
    text = "".join([chr(ord('a') + i) for i in indices])
    return text


def input_answer(driver):
    # input
    input_box = WebDriverWait(driver, 10, 0.2).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[4]/div[1]/div[1]/span[2]/div/input"))
    )
    # Ensure the input box is visible and enabled
    driver.execute_script("arguments[0].scrollIntoView(true);", input_box)
    WebDriverWait(driver, 10, 0.2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div[1]/div[1]/span[2]/div/input")))
    # Add a slight delay
    time.sleep(0.2)
    # Send keys to the input box
    input_box.send_keys(encoding_to_text(random_encoding()))
    # submit
    input_box.send_keys(Keys.RETURN)


def download_image(image_data, image_name):
    # Make sure the save directory exists
    save_directory = "./data"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    image_path = os.path.join(save_directory, image_name)
    image_base64_str = image_data.split(',')[1]  # Get the base64 part after the comma
    image_data_bytes = base64.b64decode(image_base64_str)
    # Write the image content to a file
    with open(image_path, 'wb') as file:
        file.write(image_data_bytes)


def main():
    url = "https://gen.caca01.com/ttcode/codeking"
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    num_games = 10
    for i in tqdm(range(num_games)):
        # go to link
        driver.get(url)
        # start practice
        start_practice_button = WebDriverWait(driver, 10, 0.2).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div[2]/button"))
        )
        driver.execute_script("arguments[0].click();", start_practice_button)
        # input answers
        for j in range(39):
            input_answer(driver)
        time.sleep(0.2)
        # collect data
        error_images = driver.find_elements(By.XPATH, '/html/body/div[2]/div[4]/div[1]/div[3]/div//img')
        error_texts = driver.find_elements(By.XPATH, '/html/body/div[2]/div[4]/div[1]/div[3]/div//div')
        error_data = []
        # Iterate over both lists to collect the data
        for image, text in zip(error_images, error_texts):
            error_info = {
                'image_src': image.get_attribute('src'),
                'error_text': text.text[-4:]
            }
            error_data.append(error_info)
        for error in error_data:
            download_image(error['image_src'], f"{error['error_text']}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main()
