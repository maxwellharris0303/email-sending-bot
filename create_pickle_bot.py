from selenium_driverless.sync import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import keyboard
import os


file_path = 'C:/credentials_url.txt'

previous_timestamp = os.path.getmtime(file_path)

while True:
    # Get the current timestamp of the file
    current_timestamp = os.path.getmtime(file_path)

    # Check if the file has been modified
    if current_timestamp != previous_timestamp:
        # File has changed, execute the desired code
        file = open(file_path, 'r', encoding='utf-8')
        # Read the entire content of the file
        credentials_url = file.read()
        print(credentials_url)
        # Close the file
        file.close()
        # Update the previous timestamp
        previous_timestamp = current_timestamp

        email_file = open('email.txt', 'r', encoding='utf-8')
        password_file = open('password.txt', 'r', encoding='utf-8')
        recovery_email_file = open('recovery_email.txt', 'r', encoding='utf-8')

        email_address = email_file.read()
        password = password_file.read()
        recovery_email = recovery_email_file.read()

        email_file.close()
        password_file.close()
        recovery_email_file.close()

        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get(credentials_url, wait_load=True)

        sleep(2)
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type=\"email\"]")
        email_input.write(email_address)

        next_button = driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
        next_button.click()

        sleep(3)
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type=\"password\"]")
        password_input.write(password)

        next_button = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
        next_button.click()

        try:
            sleep(5)
            challenges = driver.find_elements(By.CSS_SELECTOR, "div[class=\"l5PPKe\"]")
            print(len(challenges))
            for challenge in challenges:
                if "Confirm your recovery email" in challenge.text:
                    challenge.click()
                    break
            sleep(3)
            recovery_email_input = driver.find_element(By.CSS_SELECTOR, "input[type=\"email\"]")
            recovery_email_input.write(recovery_email)
            next_button = driver.find_elements(By.CSS_SELECTOR, "button[type=\"button\"]")[0]
            next_button.click()
        except:
            pass

        sleep(5)
        try:
            buttons = driver.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                if "Continue" in button.text:
                    button.click()
                    break
        except:
            sleep(5)
            buttons = driver.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                if "Continue" in button.text:
                    button.click()
                    break

        sleep(5)
        try:
            continue_button = driver.find_element(By.XPATH, '//*[@id="submit_approve_access"]/div/button')
            continue_button.click()
        except:
            sleep(3)
            continue_button = driver.find_element(By.XPATH, '//*[@id="submit_approve_access"]/div/button')
            continue_button.click()
        sleep(2)
        driver.quit()

    # Wait for some time before checking again
    sleep(1)  # Adjust the sleep duration as needed