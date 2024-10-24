import pycaret
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
data_df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv")



print(data_df.info())
print(data_df.describe(include='all'))

print(f'The dataset contains {data_df.shape[0]} rows and {data_df.shape[1]} columns.')


print(data_df.isnull().sum())
sns.heatmap(data_df.isnull(), cbar=False)
plt.title('Heatmap of Missing Values')
plt.show()

numerical_cols = data_df.select_dtypes(include=['float64', 'int64']).columns
print(numerical_cols)

print(data_df[numerical_cols].describe())

categorical_cols = data_df.select_dtypes(include=['object']).columns
print(categorical_cols)
for col in categorical_cols:
    print(data_df[col].value_counts())


for col in numerical_cols:
    plt.figure(figsize=(8, 6))
    sns.histplot(data_df[col], kde=True, bins=30)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.show()



for col in numerical_cols:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=data_df[col])
    plt.title(f'Box Plot of {col}')
    plt.xlabel(col)
    plt.show()



for col in categorical_cols:
    plt.figure(figsize=(8, 6))
    sns.countplot(y=data_df[col], order=data_df[col].value_counts().index)
    plt.title(f'Count Plot of {col}')
    plt.xlabel('Count')
    plt.ylabel(col)
    plt.show()

plt.figure(figsize=(10, 8))
corr = data_df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

sns.pairplot(data_df[numerical_cols])
plt.show()


for num_col in numerical_cols:
    for cat_col in categorical_cols:
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=cat_col, y=num_col, data=data_df)
        plt.title(f'{num_col} by {cat_col}')
        plt.show()


for num_col in numerical_cols:
    plt.figure(figsize=(8, 6))
    data_df.groupby('gender')[num_col].mean().plot(kind='bar')
    plt.title(f'Average {num_col} by Gender')
    plt.ylabel(f'Average {num_col}')
    plt.show()
