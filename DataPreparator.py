import argparse

from sklearn.preprocessing import StandardScaler
import pandas as pd
import datetime


class DataPreparator():
    def __init__(self, csv_file_path: str):
        self.original_df = pd.read_csv(csv_file_path)
        self.df = self.original_df.copy()

    def clean_data(self) -> int:
        initial_count = len(self.df)
        self.df.dropna(inplace=True, subset=["Czas Początkowy Podróży", "Czas Końcowy Podróży"], how='any')
        self.df.dropna(inplace=True, thresh=4)
        self.df.reset_index(inplace=True, drop=True)

        deleted_rows = initial_count - len(self.df)
        return deleted_rows

    @staticmethod
    def is_time_valid(time_str: str) -> bool:
        try:
            datetime.datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False

    def validate_time(self) -> int:
        changes_count = [0]  # Using a list to hold the count so it remains mutable
        self.df["is_valid_start_time"] = self.df["Czas Początkowy Podróży"].apply(DataPreparator.is_time_valid)
        self.df["is_valid_end_time"] = self.df["Czas Końcowy Podróży"].apply(DataPreparator.is_time_valid)

        self.df.loc[self.df["is_valid_start_time"] == False, "Czas Początkowy Podróży"] = self.df.loc[
            self.df["is_valid_start_time"] == False, "Czas Początkowy Podróży"].apply(
            lambda x: DataPreparator.fix_invalid_time(x, changes_count))
        self.df.loc[self.df["is_valid_end_time"] == False, "Czas Końcowy Podróży"] = self.df.loc[
            self.df["is_valid_end_time"] == False, "Czas Końcowy Podróży"].apply(
            lambda x: DataPreparator.fix_invalid_time(x, changes_count))

        self.df.drop(axis=1, columns=["is_valid_end_time", "is_valid_start_time"], inplace=True)
        return changes_count[0]

    @staticmethod
    def calculate_travel_time_hours(row) -> tuple[str, float]:
        time_start = row["Czas Początkowy Podróży"]
        time_end = row["Czas Końcowy Podróży"]

        diff: datetime.timedelta = datetime.datetime.strptime(time_end, "%H:%M") - datetime.datetime.strptime(
            time_start,
            "%H:%M")
        if diff.days < 0:
            diff += datetime.timedelta(days=1)

        hours, rem = divmod(diff.seconds, 3600)
        minutes = divmod(rem, 60)[0]
        return f"{hours:02}:{minutes:02}", hours + minutes / 60.0

    def drop_too_long_travels(self) -> int:
        initial_count = len(self.df)
        self.df = self.df[self.df["Total Hours"] <= 12]
        self.df.reset_index(drop=True, inplace=True)
        deleted_rows = initial_count - len(self.df)
        self.df.drop(columns=["Total Hours"], inplace=True)
        return deleted_rows

    @staticmethod
    def fix_invalid_time(time_str: str, changes_count):
        try:
            time_datetime = datetime.datetime.strptime(time_str, "%H:%M").time().strftime("%H:%M")
            return time_datetime
        except ValueError:
            hour, minute = map(int, time_str.split(":"))
            if hour >= 24:
                hour -= 24
                changes_count[0] += 1  # Increment the counter when a change is made
            time = datetime.datetime.strptime(f"{hour}:{minute}", "%H:%M").time().strftime("%H:%M")
            return time

    def fill_missing_categorical_data(self) -> int:
        before_fill = self.df.isnull().sum()
        self.df["Płeć"] = self.df["Płeć"].ffill()
        self.df["Wykształcenie"] = self.df["Wykształcenie"].bfill()
        self.df["Cel Podróży"] = self.df["Cel Podróży"].bfill()

        after_fill = self.df.isnull().sum()
        changes = before_fill - after_fill
        return changes.sum()

    def fill_missing_numerical_data(self) -> int:
        before_fill = self.df.isnull().sum()
        self.df["Wiek"] = self.df["Wiek"].interpolate(method="polynomial", axis="rows", order=2).round(2)
        self.df["Średnie Zarobki"] = self.df["Średnie Zarobki"].interpolate(method="polynomial", axis="rows",
                                                                            order=2).round(2)
        after_fill = self.df.isnull().sum()
        changes = before_fill - after_fill
        return changes.sum()

    def hot_encode(self) -> int:
        original_shape = self.df.shape

        gender_one_hot = pd.get_dummies(self.df["Płeć"], prefix="Płeć", prefix_sep="_")
        education_one_hot = pd.get_dummies(self.df["Wykształcenie"], prefix="Wykształcenie", prefix_sep="_")
        travel_target_one_hot = pd.get_dummies(self.df["Cel Podróży"], prefix="Cel Podróży", prefix_sep="_")

        self.df.drop(columns=["Płeć", "Wykształcenie", "Cel Podróży"], inplace=True)
        self.df = self.df.join([gender_one_hot, education_one_hot, travel_target_one_hot])

        new_shape = self.df.shape
        added_columns = new_shape[1] - original_shape[1]
        non_zero_entries = self.df.iloc[:, -added_columns:].astype(bool).sum().sum()

        return non_zero_entries

    def standarize_data(self) -> int:
        scaler = StandardScaler()
        standardized_columns = ["Wiek", "Średnie Zarobki"]
        self.df[standardized_columns] = scaler.fit_transform(self.df[standardized_columns])

        changed_values = self.df[standardized_columns].shape[0] * len(standardized_columns)
        return changed_values

    def prepare_data(self) -> None:
        deleted_rows = self.clean_data()
        changed_data_cells = self.validate_time()

        time_data = self.df.apply(DataPreparator.calculate_travel_time_hours, axis="columns", result_type="expand")
        self.df["Całkowity Czas Podróży"] = time_data[0]
        self.df["Total Hours"] = time_data[1]

        deleted_rows += self.drop_too_long_travels()
        changed_data_cells += self.fill_missing_categorical_data()
        changed_data_cells += self.fill_missing_numerical_data()
        changed_data_cells += self.standarize_data()
        changed_data_cells += self.hot_encode()

        self.df.to_csv("prepared.csv", index=False)

        print(f"Total amount of changed cells: {changed_data_cells}")
        print(f"Total amount of deleted rows: {deleted_rows}")
        print(f"Total amount of added columns: {self.df.shape[1] - self.original_df.shape[1]}")


def main():
    data_preparator = DataPreparator("test_data.csv")
    data_preparator.prepare_data()


if __name__ == "__main__":
    main()
