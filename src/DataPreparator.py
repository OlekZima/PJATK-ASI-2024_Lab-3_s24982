from sklearn.preprocessing import StandardScaler
import pandas as pd
import datetime
import logging

logger = logging.getLogger(__name__)


class DataPreparator:
    def __init__(self, data_df: pd.DataFrame):
        logging.basicConfig(filename="log.txt", encoding="utf-8", level=logging.INFO)

        logger.info("Starting script to prepare data")
        self.original_df = data_df

        logger.info("Created copy of the original dataframe")
        self.df = self.original_df.copy()

    def clean_data(self) -> int:
        logger.info("Starting to clean data from empty values")
        initial_count = len(self.df)

        self.df.dropna(inplace=True, subset=["Czas Początkowy Podróży", "Czas Końcowy Podróży"], how="any", axis="rows")
        self.df.dropna(inplace=True, thresh=4, axis="rows")
        self.df.reset_index(inplace=True, drop=True)

        print(self.df.isnull().sum())
        print(self.df.dtypes)

        deleted_rows = initial_count - len(self.df)
        logger.info("Finished cleaning data from empty values")
        logger.info(f"Deleted {deleted_rows} rows from original dataframe")

        print(f"Deleted {deleted_rows} rows from original dataframe due to cleaning rows with too little data")
        return deleted_rows

    @staticmethod
    def is_time_valid(time_str: str) -> bool:
        logger.info(f"Checking if time string {time_str} is valid")
        try:
            datetime.datetime.strptime(time_str, '%H:%M')
            logger.info(f"Time string {time_str} is valid")
            return True
        except ValueError:
            logger.warning(f"Time string {time_str} is not valid")
            return False

    def validate_time(self) -> int:
        logger.info("Starting to validate time strings")
        changes_count = [0]
        self.df["is_valid_start_time"] = self.df["Czas Początkowy Podróży"].apply(DataPreparator.is_time_valid)
        self.df["is_valid_end_time"] = self.df["Czas Końcowy Podróży"].apply(DataPreparator.is_time_valid)

        self.df.to_csv("test.csv", index=False)

        self.df.loc[self.df["is_valid_start_time"] == False, "Czas Początkowy Podróży"] = self.df.loc[
            self.df["is_valid_start_time"] == False, "Czas Początkowy Podróży"].apply(
            lambda x: DataPreparator.fix_invalid_time(x, changes_count))
        self.df.loc[self.df["is_valid_end_time"] == False, "Czas Końcowy Podróży"] = self.df.loc[
            self.df["is_valid_end_time"] == False, "Czas Końcowy Podróży"].apply(
            lambda x: DataPreparator.fix_invalid_time(x, changes_count))

        self.df.drop(axis=1, columns=["is_valid_end_time", "is_valid_start_time"], inplace=True)
        logger.info("Finished validating time strings")
        logger.info(f"Changes count: {changes_count}")

        print(f"Changes count: {changes_count} due to time validation")
        return changes_count[0]

    @staticmethod
    def calculate_travel_time_hours(row) -> tuple[str, float]:
        logger.info(f"Calculating travel time hours for row")
        time_start = row["Czas Początkowy Podróży"]
        time_end = row["Czas Końcowy Podróży"]

        diff: datetime.timedelta = datetime.datetime.strptime(time_end, "%H:%M") - datetime.datetime.strptime(
            time_start,
            "%H:%M")
        if diff.days < 0:
            diff += datetime.timedelta(days=1)

        hours, rem = divmod(diff.seconds, 3600)
        minutes = divmod(rem, 60)[0]
        logger.info(f"Calculated travel time hours {hours} minutes {minutes}")
        return f"{hours:02}:{minutes:02}", hours + minutes / 60.0

    def drop_too_long_travels(self) -> int:
        logger.info("Starting to drop too long travels")
        initial_count = len(self.df)
        self.df = self.df[self.df["Total Hours"] <= 12]
        self.df.reset_index(drop=True, inplace=True)
        deleted_rows = initial_count - len(self.df)
        self.df.drop(columns=["Total Hours"], inplace=True)

        logger.info("Finished dropping rows with too long time travels")
        logger.info(f"Deleted {deleted_rows} rows from original dataframe")

        print(f"Deleted {deleted_rows} rows from original dataframe due to too long travels")
        return deleted_rows

    @staticmethod
    def fix_invalid_time(time_str: str, changes_count):
        logger.info(f"Trying to fix invalid time string {time_str}")

        if time_str == "":
            logger.warning("Time is empty!")
            return "00:00"

        try:
            time_datetime = datetime.datetime.strptime(time_str, "%H:%M").time().strftime("%H:%M")
            logger.info(f"Time string {time_str} is valid")
            return time_datetime
        except ValueError:
            logger.warning(f"Time string {time_str} is not valid")
            hour, minute = map(int, time_str.split(":"))
            if hour >= 24:
                hour -= 24
                changes_count[0] += 1
            time = datetime.datetime.strptime(f"{hour}:{minute}", "%H:%M").time().strftime("%H:%M")
            logger.info(f"Time string is fixed")
            return time

    def fill_missing_categorical_data(self) -> int:
        logger.info("Starting to fill missing categorical data")
        before_fill = self.df.isnull().sum()
        self.df["Płeć"] = self.df["Płeć"].ffill()
        self.df["Wykształcenie"] = self.df["Wykształcenie"].bfill()
        self.df["Cel Podróży"] = self.df["Cel Podróży"].bfill()

        after_fill = self.df.isnull().sum()
        changes = before_fill - after_fill
        logger.info("Finished filling missing categorical data")
        logger.info(f"Filling count: {changes.sum()}")

        print(f"Added {changes.sum()} due to filling missing categorical data")
        return changes.sum()

    def fill_missing_numerical_data(self) -> int:
        logger.info("Starting to fill missing numerical data")
        before_fill = self.df.isnull().sum()
        self.df["Wiek"] = self.df["Wiek"].interpolate(method="polynomial", axis="rows", order=2).round(2)
        self.df["Średnie Zarobki"] = self.df["Średnie Zarobki"].interpolate(method="polynomial", axis="rows",
                                                                            order=2).round(2)
        after_fill = self.df.isnull().sum()
        changes = before_fill - after_fill

        logger.info("Finished filling missing numerical data")
        logger.info(f"Filling count: {changes.sum()}")

        print(f"Added {changes.sum()} due to filling missing numerical data")
        return changes.sum()

    def hot_encode(self) -> int:
        logger.info("Starting to hot encode")
        original_shape = self.df.shape

        gender_one_hot = pd.get_dummies(self.df["Płeć"], prefix="Płeć", prefix_sep="_")
        education_one_hot = pd.get_dummies(self.df["Wykształcenie"], prefix="Wykształcenie", prefix_sep="_")
        travel_target_one_hot = pd.get_dummies(self.df["Cel Podróży"], prefix="Cel Podróży", prefix_sep="_")

        self.df.drop(columns=["Płeć", "Wykształcenie", "Cel Podróży"], inplace=True)
        self.df = self.df.join([gender_one_hot, education_one_hot, travel_target_one_hot])

        new_shape = self.df.shape
        added_columns = new_shape[1] - original_shape[1]
        non_zero_entries = self.df.iloc[:, -added_columns:].astype(bool).sum().sum()
        logger.info("Finished hot encode")
        logger.info(f"Added {non_zero_entries} cells")
        logger.info(f"Added {added_columns} columns")

        print(f"Added {non_zero_entries} due to one hot encoding")
        print(f"Added {added_columns} columns")
        return non_zero_entries

    def standardize_data(self) -> int:
        logger.info("Starting to standardize data")
        scaler = StandardScaler()
        standardized_columns = ["Wiek", "Średnie Zarobki"]
        self.df[standardized_columns] = scaler.fit_transform(self.df[standardized_columns])

        changed_values = self.df[standardized_columns].shape[0] * len(standardized_columns)

        logger.info("Finished standardize data")
        logger.info(f"Changed count: {changed_values}")

        print(f"Changed {changed_values} due to standardizing data")
        return changed_values

    def prepare_data(self) -> None:
        logger.info("Trying to prepare data")
        try:
            deleted_rows = self.clean_data()
            changed_data_cells = self.validate_time()

            time_data = self.df.apply(DataPreparator.calculate_travel_time_hours, axis="columns", result_type="expand")

            logger.info("Added 'Całkowity Czas Podróży' column")
            self.df["Całkowity Czas Podróży"] = time_data[0]
            self.df["Total Hours"] = time_data[1]

            deleted_rows += self.drop_too_long_travels()
            changed_data_cells += self.fill_missing_categorical_data()
            changed_data_cells += self.fill_missing_numerical_data()
            changed_data_cells += self.standardize_data()
            changed_data_cells += self.hot_encode()

            self.df.to_csv("prepared.csv", index=False)

            assert self.df.isnull().sum().sum() == 0

            logger.info(f"Changed count: {changed_data_cells}")
            logger.info(f"Deleted count: {deleted_rows}")

            print(f"Overall amount of deleted rows: {deleted_rows}")
            print(f"Overall amount of changed cells: {changed_data_cells}")

            with open("raport.txt", "w") as f:
                f.write(f"""
                Total amount of changed cells: {changed_data_cells}
                Total amount of deleted rows: {deleted_rows}
                Total amount of added columns: {self.df.shape[1] - self.original_df.shape[1]}
                """)

            logger.info("Finished prepare data")
        except Exception as e:
            logger.critical("An exception occurred")
            logger.critical(e)
            raise e

if __name__ == "__main__":
    preparator = DataPreparator(pd.read_csv("../Lab-2-ASI - Sheet1.csv"))
    preparator.prepare_data()