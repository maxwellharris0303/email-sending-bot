from selenium_driverless.sync import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from urllib.parse import urlparse, parse_qs
import json
import quickstart_gmail_api
import quickstart

quickstart.main()
email_list = quickstart.getEmailList()
password_list = quickstart.getPasswordList()
recovery_email_list = quickstart.getRecoveryEmailList()
profile_status_list = quickstart.getProfileStatusList()
recipients_list = quickstart.getRecipientsList()
email_subject_list = quickstart.getEmailSubjectList()
email_body_list=  quickstart.getEmailBodyList()

count = len(email_list)

last_index = quickstart.getLastIndex()
print(last_index)

index = last_index
for _ in range(count):

    # EMAIL_ADDRESS = "Annahirefeedbirds@gmail.com"
    # PASSWORD = "Siraj@333"
    if profile_status_list[index] == "Disabled":
        index += 1
        continue

    EMAIL_ADDRESS = email_list[index]
    PASSWORD = password_list[index]
    RECOVERY_EMAIL_ADDRESS = recovery_email_list[index]

    email_file = open('email.txt', 'w', encoding='utf-8')
    password_file = open('password.txt', 'w', encoding='utf-8')
    recovery_email_file = open('recovery_email.txt', 'w', encoding='utf-8')
    email_file.write(EMAIL_ADDRESS)
    password_file.write(PASSWORD)
    recovery_email_file.write(RECOVERY_EMAIL_ADDRESS)
    email_file.close()
    password_file.close()
    recovery_email_file.close()

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get("https://console.cloud.google.com/", wait_load=True)
    driver.maximize_window()

    sleep(2)
    email_input = driver.find_element(By.CSS_SELECTOR, "input[type=\"email\"]")
    email_input.write(EMAIL_ADDRESS)

    next_button = driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
    next_button.click()

    sleep(3)
    try:
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type=\"password\"]")
        password_input.write(password_list[index])

        next_button = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
        next_button.click()
    except:
        driver.quit()
        RANGE_NAME = f'Sheet1!D{index + 2}:D'
        quickstart.insertStatusInfo(RANGE_NAME, "Disabled")
        index += 1
        continue
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
        recovery_email_input.write(RECOVERY_EMAIL_ADDRESS)
        next_button = driver.find_elements(By.CSS_SELECTOR, "button[type=\"button\"]")[0]
        next_button.click()
    except:
        pass

    RANGE_NAME = f'Sheet1!D{index + 2}:D'
    quickstart.insertStatusInfo(RANGE_NAME, "Active")
    sleep(3)
    driver.get("https://console.cloud.google.com/", wait_load=True)
    sleep(6)
    COUNTRY_NAME = "Finland"
    country_select_dropdown_button = driver.find_element(By.CSS_SELECTOR, "div[class=\"cfc-select-value ng-star-inserted\"]")
    country_select_dropdown_button.click()
    sleep(2)
    countries = driver.find_elements(By.CSS_SELECTOR, "span[class=\"mdc-list-item__primary-text\"]")
    print(len(countries))
    for country in countries:
        print(country.text.strip())
        if COUNTRY_NAME == country.text.strip():
            country.click()
            break
    sleep(2)
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[class=\"mdc-checkbox__native-control\"]")
    for checkbox in checkboxes:
        checkbox.click()
    sleep(3)
    agree_button = driver.find_elements(By.CSS_SELECTOR, "button[class=\"mdc-button mat-mdc-button mat-primary mat-mdc-button-base gmat-mdc-button cm-button\"]")[1]
    agree_button.click()

    sleep(3)
    select_project_button = driver.find_element(By.CSS_SELECTOR, "button[data-prober=\"cloud-console-core-functions-project-switcher\"]")
    select_project_button.click()
    sleep(3)
    try:
        new_project_button = driver.find_element(By.CSS_SELECTOR, "button[class=\"purview-picker-create-project-button mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base gmat-mdc-button cm-button ng-star-inserted\"]")
        new_project_button.click()
    except:
        sleep(5)
        new_project_button = driver.find_element(By.CSS_SELECTOR, "button[class=\"purview-picker-create-project-button mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base gmat-mdc-button cm-button ng-star-inserted\"]")
        new_project_button.click()
    sleep(5)
    project_name_input = driver.find_element(By.CSS_SELECTOR, "input[aria-describedby=\"mat-mdc-hint-2\"]")
    project_name_input.clear()
    project_name_input.write("gmailapiproject")

    create_button = driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
    create_button.click()

    sleep(10)
    try:
        select_create_button = driver.find_element(By.CSS_SELECTOR, "button[class=\"cfc-notification-action-button mdc-button mat-mdc-button mat-primary mat-mdc-button-base gmat-mdc-button cm-button ng-star-inserted\"]")
        select_create_button.click()
    except:
        sleep(5)
        select_create_button = driver.find_element(By.CSS_SELECTOR, "button[class=\"cfc-notification-action-button mdc-button mat-mdc-button mat-primary mat-mdc-button-base gmat-mdc-button cm-button ng-star-inserted\"]")
        select_create_button.click()

    sleep(3)
    print(driver.current_url)
    parsed_url = urlparse(driver.current_url)
    query_params = parse_qs(parsed_url.query)
    project_id = query_params.get('project')[0]
    print(project_id)

    enable_gmail_api_url = f"https://console.cloud.google.com/apis/library/gmail.googleapis.com?project={project_id}"
    driver.get(enable_gmail_api_url, wait_load=True)

    sleep(4)
    try:
        enable_button = driver.find_elements(By.CSS_SELECTOR, "button[aria-label=\"enable this API\"]")[1]
        enable_button.click()
    except:
        enable_button = driver.find_elements(By.CSS_SELECTOR, "button[class=\"mdc-button mdc-button--raised mat-mdc-raised-button mat-primary mat-mdc-button-base gmat-mdc-button cm-button cfc-tooltip cfc-tooltip-disable-user-select-on-touch-device ng-star-inserted\"]")[1]
        enable_button.click()

    sleep(5)
    oauth_consent_screen_url = f"https://console.cloud.google.com/apis/credentials/consent?project={project_id}"
    driver.get(oauth_consent_screen_url, wait_load=True)

    sleep(5)
    radion_button = driver.find_elements(By.CSS_SELECTOR, "input[type=\"radio\"]")[1]
    radion_button.click()
    sleep(0.5)
    create_button = driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
    create_button.click()

    sleep(4)
    try:
        close_callout_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label=\"Close callout\"]")
        close_callout_button.click()
    except:
        pass
    sleep(2)
    try:
        app_name_input = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname=\"displayName\"]")
        print(app_name_input)
        app_name_input.write("Gmailapiproject")
    except:
        sleep(3)
        app_name_input = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname=\"displayName\"]")
        print(app_name_input)
        app_name_input.write("Gmailapiproject")


    support_email_dropdown = driver.find_element(By.CSS_SELECTOR, "cm-icon[class=\"cfc-icon-small-medium-arrow ng-star-inserted\"]")
    support_email_dropdown.click()
    sleep(2)
    select_email_button = driver.find_element(By.CSS_SELECTOR, "mat-option[class=\"mat-mdc-option mdc-list-item ng-star-inserted\"]")
    select_email_button.click()
    # keyboard.press('tab')
    # keyboard.release('tab')

    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if "Got it" in button.text:
            button.click()
            sleep(2)
            break
    sleep(2)
    input_email = driver.find_element(By.CSS_SELECTOR, "input[aria-label=\"Text field for emails\"]")
    input_email.write(EMAIL_ADDRESS)
    # keyboard.press('tab')
    # keyboard.release('tab')
    sleep(2)
    save_and_continue_button = driver.find_element(By.CSS_SELECTOR, "button[class=\"cfc-stepper-step-button cfc-stepper-step-continue-button mdc-button mdc-button--raised mat-mdc-raised-button mat-unthemed mat-mdc-button-base gmat-mdc-button cm-button ng-star-inserted\"]")
    save_and_continue_button.click()
    # sleep(0.5)
    # save_and_continue_button.click()
    while True:
        try:
            sleep(3)
            save_and_continue_button = driver.find_element(By.CSS_SELECTOR, "button[class=\"cfc-stepper-step-button cfc-stepper-step-continue-button mdc-button mdc-button--raised mat-mdc-raised-button mat-unthemed mat-mdc-button-base gmat-mdc-button cm-button ng-star-inserted\"]")
            save_and_continue_button.click()
            break
        except:
            pass

    sleep(3)
    add_users_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label=\"Add users\"]")
    add_users_button.click()
    sleep(3)
    input_email = driver.find_elements(By.CSS_SELECTOR, "input[aria-label=\"Text field for emails\"]")[1]
    input_email.write(EMAIL_ADDRESS)
    sleep(1.5)
    add_button = driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
    add_button.click()
    sleep(1)
    try:
        add_button.click()
    except:
        pass

    sleep(2)
    save_and_continue_button = driver.find_element(By.CSS_SELECTOR, "button[class=\"cfc-stepper-step-button cfc-stepper-step-continue-button mdc-button mdc-button--raised mat-mdc-raised-button mat-unthemed mat-mdc-button-base gmat-mdc-button cm-button ng-star-inserted\"]")
    save_and_continue_button.click()

    sleep(3)
    credential_url = f"https://console.cloud.google.com/apis/credentials/oauthclient?previousPage=%2Fapis%2Fcredentials%3Fproject%3D{project_id}&project={project_id}"
    driver.get(credential_url, wait_load=True)
    sleep(5)

    application_type_dropdown = driver.find_element(By.CSS_SELECTOR, "cm-icon[class=\"cfc-icon-small-medium-arrow ng-star-inserted\"]")
    application_type_dropdown.click()

    options = driver.find_elements(By.TAG_NAME, 'mat-option')
    print(len(options))
    options[5].click()

    create_button = driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
    create_button.click()
    sleep(8)
    try:
        credentials_text = driver.find_element(By.TAG_NAME, 'services-client-dialog-actions').text
    except:
        sleep(5)
        credentials_text = driver.find_element(By.TAG_NAME, 'services-client-dialog-actions').text
    print(credentials_text)
    split_string = credentials_text.split()
    print(split_string)

    client_id = split_string[2]
    client_secret = split_string[5]
    print(client_id)
    print(client_secret)

    data = {
        "installed": {
            "client_id": client_id,
            "project_id": project_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": client_secret,
            "redirect_uris": [
                "http://localhost"
            ]
        }
    }

    json_data = json.dumps(data)

    file_path = f"credentials/{project_id}.json"

    with open(file_path, "w") as file:
        file.write(json_data)

    sleep(3)


    service = quickstart_gmail_api.gmail_authenticate(EMAIL_ADDRESS, project_id)
    # aaa = quickstart_gmail_api.send_message(service, "oscarrogers303@gmail.com", "Hi, Oscar", "How are you doing?")
    # print(aaa)
    

    recipients = recipients_list[index].split(", ")
    print(recipients)

    for recipient in recipients:
        EMAIL_TITLE = email_subject_list[index]
        EMAIL_BODY = f"""
        <html lang="en">
        <head> </head>
        <body>
            <div dir="ltr">
                {email_body_list[index]}
            </div>
            <img src="http://95.216.67.244/image/{EMAIL_ADDRESS}/{recipient}/image.gif" alt="image" width="1" height="1" style="display:none;">
        </body>
        </html>
        """
        try:
            aaa = quickstart_gmail_api.send_message(service, recipient, EMAIL_TITLE, EMAIL_BODY)
            print(aaa)
            if aaa['labelIds'][0] != "SENT":
                break
        except:
            sleep(30)
            pass

    print("Email Sending Done!")
    RANGE_NAME = f'Sheet1!N{index + 2}:N'
    quickstart.insertStatusInfo(RANGE_NAME, "Done")

    driver.quit()

    index += 1