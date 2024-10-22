import argparse
import logging

from src.GoogleSheeter import GoogleSheeter

logger = logging.getLogger(__name__)


def parse_args() -> tuple[str, str, str]:
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


def main() -> None:
    logging.basicConfig(filename="log.txt", encoding="utf-8", level=logging.INFO)
    logger.info("Starting the script to upload data to Google Spreadsheet")

    cred, spreadsheet, file = parse_args()

    google_sheeter = GoogleSheeter(cred, spreadsheet)
    data = google_sheeter.read_csv(file)

    google_sheeter.clear_sheet(1)
    google_sheeter.upload_csv_to_sheet(data, 1)

    logger.info("End of the uploading data to the Spreadsheet")


if __name__ == "__main__":
    main()
