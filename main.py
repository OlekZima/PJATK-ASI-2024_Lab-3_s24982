from pycaret.regression import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

url = "https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv"
data_df = pd.read_csv(url)

print(data_df.head())

print()

sns.histplot(data_df["score"], kde=True)
plt.show()

# sns.heatmap(data_df.corr(), annot=True)
# plt.show()

# sns.pairplot(data_df)
# plt.show()

clf = setup(data=pd.read_csv(url), target="score", use_gpu=True)
print(get_config('X_train'))