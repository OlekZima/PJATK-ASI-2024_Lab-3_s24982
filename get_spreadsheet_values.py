import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


def main():
    credentials_info = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
    if credentials_info is None:
        raise ValueError("GOOGLE_SHEETS_CREDENTIALS environment variable not set")

    credentials_data = json.loads(credentials_info)
    credentials = service_account.Credentials.from_service_account_info(credentials_data, scopes=SCOPES)

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:C6").execute()
        values = result.get("values", [])

        for row in values:
            print(row)

    except HttpError as err:
        print(f"An error occurred: {err}")


if __name__ == "__main__":
    main()
