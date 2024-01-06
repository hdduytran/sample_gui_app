import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


class Sheet():
    # Load the credentials from the JSON key file
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "disco-freedom-410216-f203bca6c7b3.json", scope)
    gc = gspread.authorize(credentials)

    def __init__(self, spreadsheet_name, worksheet_name=None):
        # Open the Google Sheet by title
        self.spreadsheet = self.gc.open(spreadsheet_name)

        # Select the desired worksheet by title
        if worksheet_name:
            self.worksheet = self.spreadsheet.worksheet(worksheet_name)
        else:
            self.worksheet = self.spreadsheet.get_worksheet(
                0)  # Use 0 for the first worksheet

    def replace(self, df):
        # Clear the existing sheet
        self.worksheet.clear()

        # Write the dataframe to the worksheet starting at cell A1
        self.worksheet.update(
            [df.columns.values.tolist()] + df.values.tolist())

    def append(self, df):
        # Append the dataframe to the existing sheet
        self.worksheet.append_rows(df.values.tolist())

    def append_replace(self, df):
        # Check if the sheet is empty
        if len(self.worksheet.get_all_values()) == 0:
            self.replace(df)
        else:
            self.append(df)

    def get_value_in_column(self, column_name):
        return self.worksheet.col_values(column_name)
