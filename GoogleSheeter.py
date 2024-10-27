import json
import csv
import logging
from typing import Any, List, Dict

import pandas as pd
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class GoogleSheeter(BaseModel):
    SCOPES: List[str] = ["https://www.googleapis.com/auth/spreadsheets"]
    cred_json: str = None
    credentials: Credentials = None
    spreadsheet_id: str = None
    service = None

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        logger.info("Creating GoogleSheeter object")
        self.process_data()
        logger.info("GoogleSheeter object has been created")

    def process_data(self) -> None:
        logger.info("Trying to find Google API Credentials")
        if self.cred_json is None:
            logger.critical("Failed to obtain Google API Credentials.")
            raise ValueError("GOOGLE_SHEETS_CREDENTIALS environment variable not set")
        logger.info("Google API Credentials has been found")

        logger.info("Trying to authenticate...")
        credentials_data = json.loads(self.cred_json)

        try:
            self.credentials = service_account.Credentials.from_service_account_info(credentials_data,
                                                                                     scopes=self.SCOPES)
            logger.info("Credentials has been created")
        except ValueError as e:
            logger.critical("Failed to build an credentials object")
            logger.critical(e)
            raise e
        except Exception as e:
            logger.critical("Failed to create credentials to the Google Spreadsheet. Exception has been raised.")
            logger.critical(e)
            raise e

        try:
            logger.info("Trying to build auth service")
            self.service = build('sheets', 'v4', credentials=self.credentials)
            logger.info("Service has been built")
        except MutualTLSChannelError as e:
            logger.critical("Failed due to `MutualTLSChannelError`")
            logger.critical(e)
            raise e
        except Exception as e:
            logger.critical("Failed to authenticate to the Google Spreadsheet. Exception has been raised.")
            logger.critical(e)
            raise e

    @staticmethod
    def read_csv(file_path: str):
        logger.info("Trying to read CSV file")
        try:
            with open(file_path, "r") as csv_file:
                reader = csv.reader(csv_file)
                csv_data = list(reader)
                logger.info("CSV file has been read")
                return csv_data
        except Exception as e:
            logger.critical("Failed to read CSV file")
            logger.critical(e)
            raise e

    def upload_csv_to_sheet(self, data: Dict, sheet_number: int) -> None:
        logger.info("Trying to upload CSV file to Google Spreadsheet API")
        try:
            sheet = self.service.spreadsheets()
            body = {"values": data}

            result = sheet.values().update(spreadsheetId=self.spreadsheet_id, range=f"Sheet{sheet_number}!A1",
                                           valueInputOption="RAW",
                                           body=body).execute()

            logger.info("CSV file has been uploaded")
            logger.info(f"{result.get('updatedCells')} cells updated while uploading")
        except HttpError as e:
            logger.critical("Failed to upload CSV to the Google Spreadsheet")
            logger.critical(e)
            raise e
        except Exception as e:
            logger.critical("Failed to upload CSV to the Google Spreadsheet. Exception has been raised.")
            logger.critical(e)
            raise e

    def read_sheet_to_dataframe(self, sheet_number: int) -> pd.DataFrame:
        logger.info("Trying to download data from Google Spreadsheet API")
        try:
            sheet = self.service.spreadsheets()

            columns_result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                                range=f"Sheet{sheet_number}!A1:O1").execute()
            logger.info(f"Result of getting data columns from spreadsheet: {columns_result}")
            columns = columns_result.get('values', [])[0]

            data_result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                             range=f"Sheet{sheet_number}!A2:G1001").execute()
            logger.info(f"Result of getting data from spreadsheet: {data_result}")

            spread_sheet_data = data_result.get('values', [])
            logger.info(f"Accessed data from result: {spread_sheet_data}")

            data_df = pd.DataFrame(spread_sheet_data, columns=columns)
            data_df[["Wiek", "Średnie Zarobki"]] = data_df[["Wiek", "Średnie Zarobki"]].apply(pd.to_numeric)
            data_df["Wiek"] = data_df["Wiek"].apply(lambda x: int(x) if pd.notna(x) else x)

            logger.info(f"Accessed data as DataFrame: {data_df}")
            return data_df

        except HttpError as e:
            logger.critical("Failed to download data from Google Spreadsheet")
            logger.critical(e)
            raise e
        except Exception as e:
            logger.critical("Failed to download data from Google Spreadsheet")
            logger.critical(e)
            raise e

    def clear_sheet(self, sheet_number: int) -> None:
        logger.info("Trying to clear Google Spreadsheet")
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().clear(spreadsheetId=self.spreadsheet_id, range=f"Sheet{sheet_number}!A1:Z",
                                          body={}).execute()
            logger.info("Google Spreadsheet has been cleared")
            logger.info(f"Cleared range: {result.get('clearedRange')}")

        except HttpError as e:
            logger.critical("Failed to clear Google Spreadsheet")
            logger.critical(e)
            raise e
        except Exception as e:
            logger.critical("Failed to clear Google Spreadsheet. Exception has been raised.")
            logger.critical(e)
            raise e
