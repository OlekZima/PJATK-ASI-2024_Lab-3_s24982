from pycaret.regression import *
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)
data_df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv")

data_df = data_df.drop(columns=["rownames"])

print(data_df.info())
print(data_df.describe(include="all"))

print(f"The dataset contains {data_df.shape[0]} rows and {data_df.shape[1]} columns.")

numerical_cols = data_df.select_dtypes(include=["float64", "int64"]).columns
print(numerical_cols)

print(data_df[numerical_cols].describe())

categorical_cols = data_df.select_dtypes(include=["object"]).columns
print(categorical_cols)
for col in categorical_cols:
    print(data_df[col].value_counts())

for col in numerical_cols:
    plt.figure(figsize=(8, 6))
    sns.histplot(data_df[col], kde=True, bins=30)
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.savefig(f"documentation/docs/img/Distribution_of_{col}.png", bbox_inches="tight")

for col in numerical_cols:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=data_df[col])
    plt.title(f"Box Plot of {col}")
    plt.xlabel(col)
    plt.savefig(f"documentation/docs/img/Boxplot_of_{col}.png", bbox_inches="tight")

for col in categorical_cols:
    plt.figure(figsize=(8, 6))
    sns.countplot(y=data_df[col], order=data_df[col].value_counts().index)
    plt.title(f"Count Plot of {col}")
    plt.xlabel("Count")
    plt.ylabel(col)
    plt.savefig(f"documentation/docs/img/Countplot_of_{col}.png", bbox_inches="tight")

# ../.../././//././..././././.

data_df["gender"] = data_df["gender"].apply(lambda x: x == "female")
data_df = data_df.rename(columns={"gender": "gender_is_female"})

data_df["fcollege"] = data_df["fcollege"].apply(lambda x: x == "yes")
data_df = data_df.rename(columns={"fcollege": "is_fcollege"})

data_df["mcollege"] = data_df["mcollege"].apply(lambda x: x == "yes")
data_df = data_df.rename(columns={"mcollege": "is_mcollege"})

data_df["home"] = data_df["home"].apply(lambda x: x == "yes")
data_df = data_df.rename(columns={"home": "is_home"})

data_df["urban"] = data_df["urban"].apply(lambda x: x == "yes")
data_df = data_df.rename(columns={"urban": "is_urban"})

data_df["income"] = data_df["income"].apply(lambda x: x == "high")
data_df = data_df.rename(columns={"income": "is_high_income"})

data_df["region"] = data_df["region"].apply(lambda x: x == "west")
data_df = data_df.rename(columns={"region": "is_region_west"})

data_df = pd.get_dummies(data_df, columns=["ethnicity"], prefix=["ethnicity"], prefix_sep="_", dtype=int)

print(data_df.head())
print(data_df.info())

plt.figure(figsize=(10, 8))
corr = data_df.corr()
corr_rounded = corr.round(2)
sns.heatmap(corr, annot=corr_rounded, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("documentation/docs/img/Correlation_Heatmap.png")

sns.pairplot(data_df)
plt.savefig("documentation/docs/img/pairplot.png")

msk = np.random.rand(len(data_df)) < 0.8
train_df = data_df[msk]
test_df = data_df[~msk]
print(train_df.shape, test_df.shape)