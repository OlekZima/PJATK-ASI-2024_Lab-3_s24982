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
    target_dir = "documentation/docs/img"
    source_dir = "./"

    os.makedirs(target_dir, exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        filename="logging.log",
        filemode="w",
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    # Also print logs to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logger = logging.getLogger(__name__)

    logger.info("Loading data...")
    pd.set_option("display.max_columns", None)
    data_df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv")

    # Record initial number of rows
    initial_row_count = data_df.shape[0]
    logger.info(f"Initial number of rows: {initial_row_count}")

    # Drop unnecessary columns
    data_df = data_df.drop(columns=["rownames"])
    logger.debug("Dropped 'rownames' column.")

    logger.info("Data information:")
    logger.info(data_df.info())

    logger.info("Data description:")
    logger.info(data_df.describe(include="all"))

    logger.info(f"The dataset contains {data_df.shape[0]} rows and {data_df.shape[1]} columns.")

    numerical_cols = data_df.select_dtypes(include=["float64", "int64"]).columns
    logger.info(f"Numerical columns: {list(numerical_cols)}")

    logger.info("Statistical summary of numerical columns:")
    logger.info(data_df[numerical_cols].describe())

    categorical_cols = data_df.select_dtypes(include=["object"]).columns
    logger.info(f"Categorical columns: {list(categorical_cols)}")
    for col in categorical_cols:
        logger.info(f"Value counts for {col}:")
        logger.info(data_df[col].value_counts())

    # Check for missing values
    missing_values_count = data_df.isnull().sum().sum()
    logger.info(f"Total missing values in data_df: {missing_values_count}")

    if missing_values_count > 0:
        # Drop rows with missing values
        before_dropna_row_count = data_df.shape[0]
        data_df = data_df.dropna()
        after_dropna_row_count = data_df.shape[0]
        rows_removed_due_to_missing = before_dropna_row_count - after_dropna_row_count
        logger.info(f"Rows removed due to missing values: {rows_removed_due_to_missing}")
    else:
        logger.info("No missing values found.")

    # Generate plots if --plots argument is provided
    if arguments.plots:
        logger.info("Generating plots...")
        # Histograms for numerical variables
        for col in numerical_cols:
            plt.figure(figsize=(8, 6))
            sns.histplot(data_df[col], kde=True, bins=30)
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.savefig(f"{target_dir}/Distribution_of_{col}.png", bbox_inches="tight")
            plt.close()

        # Box plots for numerical variables
        for col in numerical_cols:
            plt.figure(figsize=(8, 6))
            sns.boxplot(x=data_df[col])
            plt.title(f"Box Plot of {col}")
            plt.xlabel(col)
            plt.savefig(f"{target_dir}/Boxplot_of_{col}.png", bbox_inches="tight")
            plt.close()

        # Count plots for categorical variables
        for col in categorical_cols:
            plt.figure(figsize=(8, 6))
            sns.countplot(y=data_df[col], order=data_df[col].value_counts().index)
            plt.title(f"Count Plot of {col}")
            plt.xlabel("Count")
            plt.ylabel(col)
            plt.savefig(f"{target_dir}/Countplot_of_{col}.png", bbox_inches="tight")
            plt.close()

    # Data preprocessing
    logger.info("Preprocessing data...")
    preprocessed_row_count = data_df.shape[0]

    # Convert categorical variables to boolean
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

    # Check for any row changes after preprocessing
    post_preprocessing_row_count = data_df.shape[0]
    rows_added = post_preprocessing_row_count - preprocessed_row_count
    logger.info(f"Rows added during preprocessing: {rows_added}")

    logger.info("Data after preprocessing:")
    logger.info(data_df.head())
    logger.info(data_df.info())

    # Generate correlation heatmap and pairplot if --plots argument is provided
    if arguments.plots:
        logger.info("Generating correlation heatmap and pairplot...")
        plt.figure(figsize=(10, 8))
        corr = data_df.corr()
        corr_rounded = corr.round(2)
        sns.heatmap(corr, annot=corr_rounded, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.savefig(f"{target_dir}/Correlation_Heatmap.png")
        plt.close()
        logger.debug("Saved correlation heatmap.")

        # Pairplot
        sns.pairplot(data_df)
        plt.savefig(f"{target_dir}/pairplot.png")
        plt.close()
        logger.debug("Saved pairplot.")

    # Split data into training and testing sets
    logger.info("Splitting data into training and testing sets...")
    msk = np.random.rand(len(data_df)) < 0.7
    train_df = data_df[msk].copy()
    test_df = data_df[~msk].copy()
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

    logger.info("Data after scaling (first five rows of training data):")
    logger.info(train_df.head())

    # Record number of rows before model setup
    original_train_rows = train_df.shape[0]
    original_test_rows = test_df.shape[0]

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
                verbose=False,
                silent=True)

    # Get the data after setup
    X_train = get_config('X_train')
    y_train = get_config('y_train')
    X_test = get_config('X_test')
    y_test = get_config('y_test')

    post_setup_train_rows = X_train.shape[0]
    post_setup_test_rows = X_test.shape[0]

    # Calculate rows removed during setup (e.g., outlier removal)
    train_rows_removed = original_train_rows - post_setup_train_rows
    test_rows_removed = original_test_rows - post_setup_test_rows

    logger.info(f"Number of rows in training data before setup: {original_train_rows}")
    logger.info(f"Number of rows in training data after setup: {post_setup_train_rows}")
    logger.info(f"Number of rows removed from training data during setup: {train_rows_removed}")

    logger.info(f"Number of rows in test data before setup: {original_test_rows}")
    logger.info(f"Number of rows in test data after setup: {post_setup_test_rows}")
    logger.info(f"Number of rows removed from test data during setup: {test_rows_removed}")

    # Compare models
    logger.info("Comparing models...")
    best_model = compare_models()
    logger.info(f"Best model: {best_model}")

    # Create and evaluate the model
    logger.info("Creating and evaluating the Bayesian Ridge Regression model...")
    model = create_model("br")
    evaluate_model(model)

    # Plotting model
    if arguments.plots:
        logger.info("Generating model plots...")
        plot_model(model, plot="residuals", save=True)
        plot_model(model, plot="vc", save=True)
        plot_model(model, plot="feature_all", save=True)
        plot_model(model, plot="error", save=True)

    # Tuning model
    logger.info("Tuning the model...")
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

    # Move plot images to target directory
    logger.info("Moving .png files to the target directory...")
    for filename in os.listdir(source_dir):
        if filename.endswith(".png"):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)

            shutil.move(source_path, target_path)
            logger.info(f"Moved {filename} to {target_path}")

    logger.info("Script execution completed.")


def parse_args():
    parser = argparse.ArgumentParser(description='ML Model Training Script')
    parser.add_argument('--plots', action='store_true', help='Generate and save plots')
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    main(arguments)
