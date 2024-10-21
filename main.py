from autogluon.tabular import TabularPredictor, TabularDataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    pd.set_option("display.max_columns", None)

    data_df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv")
    print(f"Head:\n{data_df.head()}\n{80*'='}")
    print(f"dtypes:\n{data_df.dtypes}\n{80*'='}")
    print(f"Info:\n{data_df.info()}\n{80 * '='}")
    print(f"describe:\n{data_df.describe()}\n{80 * '='}")

    data_df = data_df.drop("rownames", axis="columns")
    print(data_df.head())

    object_columns = ["gender", "ethnicity", "fcollege", "mcollege", "home", "urban", "income", "region"]
    for col in object_columns:
        data_df[col] = pd.Categorical(data_df[col])
    cat_columns = data_df.select_dtypes(["category"]).columns
    print(cat_columns)

    data_df[cat_columns] = data_df[cat_columns].apply(lambda x: x.cat.codes)
    print(data_df.head())




if __name__ == '__main__':
    main()
