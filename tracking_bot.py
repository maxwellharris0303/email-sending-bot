from flask import Flask, request
from flask_cors import CORS
import re
import quickstart


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

# @app.route('/start-bot', methods=['POST'])
# def start_upwork_bot():
#     print("Hello")

#     return "Done"

@app.before_request
def before_request():
    # Perform any monitoring or logging actions here
    REQUEST_PATH = request.path
    # REQUEST_METHOD = request.method
    # print(f"Incoming request: {REQUEST_METHOD} {REQUEST_PATH}")

    matches = re.findall(pattern, REQUEST_PATH)

    sender_email = ""
    recipient_email = ""
    if len(matches) == 2:
        sender_email = matches[0]
        recipient_email = matches[1]
        # Print the extracted email addresses
        print(f"Sender email: {sender_email}")
        print(f"Recipient email: {recipient_email}")

        # sender_email = "Sara.feedbird45@gmail.com"

        quickstart.main()
        email_list = quickstart.getEmailList()
        opened_recipients_list = quickstart.getOpenedRecipientsList()
        total_opening_count_list = quickstart.getTotalOpeningCountList()
        # print(email_list)
        index = 0
        for email in email_list:
            if email == sender_email:
                break
            index += 1

        if len(email_list) != index:
            # print(index)
            # RANGE_NAME = f'Sheet1!O{index + 2}:O'
            # if total_opening_count_list[index] == "no":
            #     quickstart.insertStatusInfo(RANGE_NAME, 1)
            # else:
            #     value_total_count = int(total_opening_count_list[index]) + 1
            #     quickstart.insertStatusInfo(RANGE_NAME, value_total_count)

            
            if opened_recipients_list[index] == "no":
                RANGE_NAME = f'Sheet1!O{index + 2}:O'
                quickstart.insertStatusInfo(RANGE_NAME, recipient_email)
                RANGE_NAME = f'Sheet1!P{index + 2}:P'
                quickstart.insertStatusInfo(RANGE_NAME, 1)
            else:
                if recipient_email not in opened_recipients_list[index]:
                    RANGE_NAME = f'Sheet1!O{index + 2}:O'
                    value_opened_recipient = str(opened_recipients_list[index]) + ", " + str(recipient_email)
                    quickstart.insertStatusInfo(RANGE_NAME, value_opened_recipient)
                    RANGE_NAME = f'Sheet1!P{index + 2}:P'
                    value_total_count = int(total_opening_count_list[index]) + 1
                    quickstart.insertStatusInfo(RANGE_NAME, value_total_count)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)