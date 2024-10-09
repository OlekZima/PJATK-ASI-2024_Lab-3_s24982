import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import argparse


def main(cred, spreadsheet):
    SCOPES: list[str] = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials_info = cred
    if credentials_info is None:
        raise ValueError("GOOGLE_SHEETS_CREDENTIALS environment variable not set")

    credentials_data = json.loads(credentials_info)
    credentials = service_account.Credentials.from_service_account_info(credentials_data, scopes=SCOPES)

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=spreadsheet, range="Sheet1!A1:C6").execute()
        values = result.get("values", [])

        for row in values:
            print(row)

    except HttpError as err:
        print(f"An error occurred: {err}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cred", type=str, help="Google Credentials", required=True)
    parser.add_argument("-s", "--spreadsheet", type=str, help="Google Spreadsheet ID", required=True)
    args = parser.parse_args()

    cred = args.cred
    spreadsheet = args.spreadsheet

    main(cred, spreadsheet)
