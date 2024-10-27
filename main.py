import argparse
import logging
import os
import shutil

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from pycaret.regression import *


def main(arguments):
    # Configure logging
    logging.basicConfig(level=logging.INFO, filename="logging.log", filemode="w")
    logger = logging.getLogger(__name__)

    logger.info("Loading data...")
    pd.set_option("display.max_columns", None)
    data_df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv")

    # Drop unnecessary columns
    data_df = data_df.drop(columns=["rownames"])
    logger.debug("Dropped 'rownames' column.")

    logger.info("Data information:")
    logger.info(data_df.info())

    logger.info("Data description:")
    logger.info(data_df.describe(include="all"))

    logger.info(f"The dataset contains {data_df.shape[0]} rows and {data_df.shape[1]} columns.")

    numerical_cols = data_df.select_dtypes(include=["float64", "int64"]).columns
    logger.info(f"Numerical columns: {numerical_cols}")

    logger.info("Statistical summary of numerical columns:")
    logger.info(data_df[numerical_cols].describe())

    categorical_cols = data_df.select_dtypes(include=["object"]).columns
    logger.info(f"Categorical columns: {categorical_cols}")
    for col in categorical_cols:
        logger.info(f"Value counts for {col}:")
        logger.info(data_df[col].value_counts())

    # Generate plots if --plots argument is provided
    if arguments:
        logger.info("Generating plots...")
        # Histograms for numerical variables
        for col in numerical_cols:
            plt.figure(figsize=(8, 6))
            sns.histplot(data_df[col], kde=True, bins=30)
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.savefig(f"documentation/docs/img/Distribution_of_{col}.png", bbox_inches="tight")
            plt.close()
            logger.debug(f"Saved histogram for {col}.")

        # Box plots for numerical variables
        for col in numerical_cols:
            plt.figure(figsize=(8, 6))
            sns.boxplot(x=data_df[col])
            plt.title(f"Box Plot of {col}")
            plt.xlabel(col)
            plt.savefig(f"documentation/docs/img/Boxplot_of_{col}.png", bbox_inches="tight")
            plt.close()
            logger.debug(f"Saved box plot for {col}.")

        # Count plots for categorical variables
        for col in categorical_cols:
            plt.figure(figsize=(8, 6))
            sns.countplot(y=data_df[col], order=data_df[col].value_counts().index)
            plt.title(f"Count Plot of {col}")
            plt.xlabel("Count")
            plt.ylabel(col)
            plt.savefig(f"documentation/docs/img/Countplot_of_{col}.png", bbox_inches="tight")
            plt.close()
            logger.debug(f"Saved count plot for {col}.")

    # Data preprocessing
    logger.info("Preprocessing data...")
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

    # One-hot encode 'ethnicity' column
    data_df = pd.get_dummies(data_df, columns=["ethnicity"], prefix=["ethnicity"], prefix_sep="_", dtype=int)
    logger.debug("Applied one-hot encoding to 'ethnicity' column.")

    logger.info("Data after preprocessing:")
    logger.info(data_df.head())
    logger.info(data_df.info())

    # Generate correlation heatmap if --plots argument is provided
    if arguments:
        logger.info("Generating correlation heatmap and pairplot...")
        plt.figure(figsize=(10, 8))
        corr = data_df.corr()
        corr_rounded = corr.round(2)
        sns.heatmap(corr, annot=corr_rounded, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.savefig("documentation/docs/img/Correlation_Heatmap.png")
        plt.close()
        logger.debug("Saved correlation heatmap.")

        # Pairplot
        sns.pairplot(data_df)
        plt.savefig("documentation/docs/img/pairplot.png")
        plt.close()
        logger.debug("Saved pairplot.")

    # Split data into training and testing sets
    logger.info("Splitting data into training and testing sets...")
    msk = np.random.rand(len(data_df)) < 0.7
    train_df = data_df[msk]
    test_df = data_df[~msk]
    logger.info(f"Training set shape: {train_df.shape}")
    logger.info(f"Testing set shape: {test_df.shape}")

    # Ensure 'education' is of type float
    data_df["education"] = data_df["education"].astype(float)

    # Scale numerical features
    logger.info("Scaling numerical features...")
    columns_to_scale = data_df.select_dtypes(include=["float64"]).columns
    scaler = StandardScaler()
    train_df[columns_to_scale] = scaler.fit_transform(train_df[columns_to_scale])
    test_df[columns_to_scale] = scaler.transform(test_df[columns_to_scale])
    logger.debug("Applied StandardScaler to numerical features.")

    logger.info("Data after scaling:")
    logger.info(train_df.head())

    # PyCaret setup
    logger.info("Setting up PyCaret regression environment...")
    reg = setup(data=train_df,
                target="score",
                test_data=test_df,
                remove_outliers=True,
                fold_strategy="kfold",
                fold=15,
                session_id=2137,
                fold_shuffle=True,
                use_gpu=True,
                normalize=True,
                index=False,
                verbose=False)

    # Compare models
    logger.info("Comparing models...")
    best_model = compare_models()
    logger.info(f"Best model: {best_model}")

    # Create and evaluate the model
    logger.info("Creating and evaluating the Gradient Boosting Regressor model...")
    model = create_model("br")
    evaluate_model(model)

    # Plotting model
    plot_model(model, plot="residuals", save=True)
    plot_model(model, plot="vc", save=True)
    plot_model(model, plot="feature_all", save=True)
    plot_model(model, plot="error", save=True)

    # Tuning model
    tuned_model = tune_model(model, n_iter=100, early_stopping=True, optimize="R2", choose_better=True)
    evaluate_model(tuned_model)

    # Make predictions
    logger.info("Making predictions on the test data...")
    predictions = predict_model(tuned_model, data=test_df)
    logger.info("Predictions:")
    logger.info(predictions.head())

    # Save the final model
    logger.info("Saving the final model...")
    save_model(tuned_model, "model")

    logger.info("Moving .png files to the mkdocs directory...")
    target_dir = "documentation/docs/img"
    source_dir = "./"

    for filename in os.listdir(source_dir):
        if filename.endswith(".png"):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)

            shutil.move(source_path, target_path)
            logger.info(f"Moved {filename} to {target_path}")



def parse_args():
    parser = argparse.ArgumentParser(description='ML Model Training Script')
    parser.add_argument('--plots', help='Generate and save plots')
    return False if parser.parse_args() == 0 else True


if __name__ == "__main__":
    arguments = parse_args()
    main(arguments)
