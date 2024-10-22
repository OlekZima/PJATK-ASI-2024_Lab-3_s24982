import argparse
import logging
from src.DataPreparator import DataPreparator
from src.GoogleSheeter import GoogleSheeter

logger = logging.getLogger(__name__)


def parse_args() -> tuple[str, str]:
    logger.info("Trying to parse arguments.")
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--cred", type=str, help="Google Credentials", required=True)
        parser.add_argument("-s", "--spreadsheet", type=str, help="Google Spreadsheet ID", required=True)
        args = parser.parse_args()

        logger.info("Arguments have been parsed.")
        return args.cred, args.spreadsheet

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
    logging.basicConfig(filename="log_get_prepare_upload.txt", encoding="utf-8", level=logging.INFO)
    logger.info("Starting the script")

    cred, spreadsheet = parse_args()

    google_sheeter = GoogleSheeter(cred, spreadsheet)
    data = google_sheeter.read_sheet_to_csv(1)  # 1 is first (1) Sheet in Spreadsheet with raw data

    google_sheeter.clear_sheet(2)  # 2 is the second (2) Sheet in Spreadsheet with prepared data
    data_preparator = DataPreparator(data)
    data_preparator.prepare_data()
    data_prepared = google_sheeter.read_csv("prepared.csv")
    google_sheeter.upload_csv_to_sheet(data_prepared, 2)

    logger.info("End of the uploading prepared data to the Spreadsheet")


if __name__ == "__main__":
    main()
