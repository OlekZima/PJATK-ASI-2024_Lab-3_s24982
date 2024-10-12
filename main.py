import csv
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse

from DataPreparator import DataPreparator


class GoogleSheeter():
    def __init__(self, cred: str, spreadsheet_id: str):
        self.SCOPES: list[str] = ["https://www.googleapis.com/auth/spreadsheets"]
        if cred is None:
            raise ValueError("GOOGLE_SHEETS_CREDENTIALS environment variable not set")
        credentials_data = json.loads(cred)

        self.credentials = service_account.Credentials.from_service_account_info(credentials_data, scopes=self.SCOPES)
        self.spreadsheet_id = spreadsheet_id
        self.service = build('sheets', 'v4', credentials=self.credentials)

    @staticmethod
    def read_csv(file_path: str) -> list:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            csv_data = list(reader)
            return csv_data

    def upload_csv_to_sheet(self, data) -> None:
        try:
            sheet = self.service.spreadsheets()
            range_sheet = "Sheet1!A1"
            body = {"values": data}

            result = sheet.values().update(spreadsheetId=self.spreadsheet_id, range=range_sheet, valueInputOption="RAW",
                                           body=body).execute()

            print(f"{result.get("updatedCells")} cells updated")

        except HttpError as e:
            print(e)

    def clear_sheet(self):
        try:
            sheet = self.service.spreadsheets()
            range_sheet = "Sheet1!A1:Z"
            body = {}
            result = sheet.values().clear(spreadsheetId=self.spreadsheet_id, range=range_sheet, body=body).execute()
            print(f"{result.get('updatedCells')} cells updated")
        except HttpError as e:
            print(e)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cred", type=str, help="Google Credentials", required=True)
    parser.add_argument("-s", "--spreadsheet", type=str, help="Google Spreadsheet ID", required=True)
    parser.add_argument("-f", "--file", type=str, help="CSV file", required=True)
    args = parser.parse_args()

    return args.cred, args.spreadsheet, args.file


def main():
    cred, spreadsheet, file = parse_args()

    google_sheeter = GoogleSheeter(cred, spreadsheet)
    data = google_sheeter.read_csv(file)

    google_sheeter.clear_sheet()
    google_sheeter.upload_csv_to_sheet(data)

    google_sheeter.clear_sheet()
    data_preparator = DataPreparator("data_student_24982.csv")
    data_preparator.prepare_data()
    data_prepared = google_sheeter.read_csv("prepared.csv")
    google_sheeter.upload_csv_to_sheet("prepared.csv")


if __name__ == "__main__":
    main()
