from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '16RlLn4vO-49a-Th5kFvUYAg2XQA2eG35T33Z1YsoZDs'
SAMPLE_RANGE_NAME = 'Sheet1!A2:P'

emailList = []

passwordList = []

recoveryEmailList = []

already_used_email_list = []

profile_status_list = []

recipients_list = []

email_subject_list = []

email_body_list = []

opened_recipients_list = []

total_opening_count_list = []

columnCount = 0


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        emailList.clear()
        passwordList.clear()
        recoveryEmailList.clear()
        already_used_email_list.clear()
        profile_status_list.clear()
        recipients_list.clear()
        email_subject_list.clear()
        email_body_list.clear()

        opened_recipients_list.clear()
        total_opening_count_list.clear()
        # print('Property Address, City:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            if len(row) >= 3:
                emailList.append('%s' % (row[0]))
                passwordList.append('%s' % (row[1]))
                recoveryEmailList.append('%s' % (row[2]))
            if len(row) >= 14:
                already_used_email_list.append('%s' % (row[0]))
            if len(row) >= 4 and str(row[3]) == "Disabled":
                profile_status_list.append("Disabled")
            else:
                profile_status_list.append("Active")

            if len(row) >= 10:
                recipients_list.append('%s' % (row[9]))
            if len(row) >= 13:
                email_subject_list.append('%s' % (row[11]))
                email_body_list.append('%s' % (row[12]))
            if len(row) >= 15:
                opened_recipients_list.append('%s' % (row[14]))
            else:
                opened_recipients_list.append("no")
            if len(row) >= 16:
                total_opening_count_list.append('%s' % (row[15]))
            else:
                total_opening_count_list.append("no")

        # print(getOpenedRecipientsList())
        # print(getTotalOpeningCountList())
        # print(getEmailList())
        # print(getPasswordList())
        # print(getRecoveryEmailList())
    except HttpError as err:
        print(err)

def getLastIndex():
    return len(already_used_email_list)

def getEmailSubjectList():
    return email_subject_list

def getEmailBodyList():
    return email_body_list

def getRecipientsList():
    return recipients_list

def getProfileStatusList():
    return profile_status_list

def getEmailList():
    return emailList

def getPasswordList():
    return passwordList

def getRecoveryEmailList():
    return recoveryEmailList

def getOpenedRecipientsList():
    return opened_recipients_list

def getTotalOpeningCountList():
    return total_opening_count_list


def getColumnCount():
    columnCount = len(emailList)
    return columnCount


def insertStatusInfo(range_name, status_info):

    
    values_status_info = [
        [status_info]
    ]
    request_body = {
        'values': values_status_info
    }


    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Finally, call the API to write the data to the spreadsheet
        result = service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=request_body
            ).execute()

        print('{0} status info updated.'.format(result.get('updatedCells')))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()