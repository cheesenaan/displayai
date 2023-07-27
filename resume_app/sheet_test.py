import gspread
from google.oauth2.service_account import Credentials

def get_google_sheet():
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('/Users/cheesenaan/Documents/projects/resume_app/project/.ipynb_checkpoints/resume_App/resume_app/resume_app/resume-app-392923-d8e95b50b335.json', scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open('resume_app').sheet1  # Replace with your actual Google Sheet name
    return sheet


def add_test_data():
    sheet = get_google_sheet()

    # Add test data to the sheet
    test_data = [
        ['John', 'Doe', 'john.doe@example.com'],
        ['Jane', 'Smith', 'jane.smith@example.com'],
        ['Bob', 'Johnson', 'bob.johnson@example.com']
    ]

    start_row = 2  # Adjust the starting row according to your sheet's structure
    start_column = 1  # Adjust the starting column according to your sheet's structure

    for i, data_row in enumerate(test_data):
        row = start_row + i
        for j, value in enumerate(data_row):
            column = start_column + j
            sheet.update_cell(row, column, value)

    print("Test data added successfully!")


add_test_data()


