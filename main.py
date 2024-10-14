import csv
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse
import logging
from google.auth.exceptions import MutualTLSChannelError
from DataPreparator import DataPreparator

logger = logging.getLogger(__name__)


class GoogleSheeter():
    def __init__(self, cred: str, spreadsheet_id: str):
        self.SCOPES: list[str] = ["https://www.googleapis.com/auth/spreadsheets"]
        logger.info("Trying to find Google API Credentials")
        if cred is None:
            logger.critical("Failed to obtain Google API Credentials.")
            raise ValueError("GOOGLE_SHEETS_CREDENTIALS environment variable not set")
        logger.info("Google API Credentials has been found")

        logger.info("Trying to authenticate...")
        credentials_data = json.loads(cred)

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

        self.spreadsheet_id = spreadsheet_id
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
    def read_csv(file_path: str) -> list:
        logger.info("Trying to read CSV file")
        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                csv_data = list(reader)
                logger.info("CSV file has been read.")
                return csv_data
        except Exception as e:
            logger.critical("Failed to read CSV file")
            logger.critical(e)
            raise e

    def upload_csv_to_sheet(self, data) -> None:
        logger.info("Trying to upload CSV file to Google Spreadsheet API")
        try:
            sheet = self.service.spreadsheets()
            body = {"values": data}

            result = sheet.values().update(spreadsheetId=self.spreadsheet_id, range="Sheet1!A1", valueInputOption="RAW",
                                           body=body).execute()

            logger.info("CSV file has been uploaded")
            logger.info(f"{result.get('deleted')} cells deleted while uploading")
        except HttpError as e:
            logger.critical("Failed to upload CSV to the Google Spreadsheet")
            logger.critical(e)
            raise e
        except Exception as e:
            logger.critical("Failed to upload CSV to the Google Spreadsheet. Exception has been raised.")
            logger.critical(e)
            raise e

    def clear_sheet(self):
        logger.info("Trying to clear Google Spreadsheet")
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().clear(spreadsheetId=self.spreadsheet_id, range="Sheet1!A1:Z", body={}).execute()
            logger.info("Google Spreadsheet has been cleared")
            logger.info(f"{result.get('deleted')} cells deleted while clearing")

        except HttpError as e:
            logger.critical("Failed to clear Google Spreadsheet")
            logger.critical(e)
            raise e
        except Exception as e:
            logger.critical("Failed to clear Google Spreadsheet. Exception has been raised.")
            logger.critical(e)
            raise e


def parse_args():
    logger.info("Trying to parse arguments.")
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--cred", type=str, help="Google Credentials", required=True)
        parser.add_argument("-s", "--spreadsheet", type=str, help="Google Spreadsheet ID", required=True)
        parser.add_argument("-f", "--file", type=str, help="CSV file", required=True)
        args = parser.parse_args()

        logger.info("Arguments have been parsed.")
        return args.cred, args.spreadsheet, args.file

    except argparse.ArgumentError as arg_error:
        logger.critical("Argument error exception. Failed to parse arguments.")
        raise arg_error
    except argparse.ArgumentTypeError as type_error:
        logger.critical("Type error exception. Failed to parse arguments.")
        raise type_error
    except Exception as e:
        logger.critical("Failed to parse arguments. Exception has been raised.")
        logger.critical(e)
        raise e


def main():
    logging.basicConfig(filename="log.txt", encoding="utf-8", level=logging.INFO)
    logger.info("Starting the script")

    cred, spreadsheet, file = parse_args()

    google_sheeter = GoogleSheeter(cred, spreadsheet)
    data = google_sheeter.read_csv(file)

    google_sheeter.clear_sheet()
    google_sheeter.upload_csv_to_sheet(data)

    google_sheeter.clear_sheet()
    data_preparator = DataPreparator("data_student_24982.csv")
    data_preparator.prepare_data()
    data_prepared = google_sheeter.read_csv("prepared.csv")
    google_sheeter.upload_csv_to_sheet(data_prepared)

    logger.info("End of the script")


if __name__ == "__main__":
    main()
