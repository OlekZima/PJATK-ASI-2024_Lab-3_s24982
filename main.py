import pandas as pd
from pycaret.regression import load_model, predict_model
import streamlit as st
from io import StringIO


class ScorePredictor:
    def __init__(self, model_path: str = "model"):
        super().__init__()
        self.model = load_model(model_path)

    @staticmethod
    def read_csv(data: StringIO) -> pd.DataFrame:
        """Reads CSV data from a string buffer and returns a DataFrame."""
        try:
            read_data = pd.read_csv(data)
            return read_data
        except pd.errors.ParserError as e:
            st.error(f"Error reading CSV: {e}")
            raise ValueError("Could not parse CSV data.") from e

    def make_predictions(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Generates predictions from a DataFrame."""
        return predict_model(self.model, data=data_frame)


# Streamlit App
st.title("Score Predictor")

file = st.file_uploader(label="Upload a CSV file with your data", type=["csv"])

if file is not None:
    stringio = StringIO(file.getvalue().decode("utf-8"))
    data_df: pd.DataFrame = ScorePredictor.read_csv(stringio)

    if data_df is not None:
        st.write("Input Data", data_df)

        predictor: ScorePredictor = ScorePredictor()
        predictions: pd.DataFrame = predictor.make_predictions(data_df)

        st.write("Predicted score is:",
                 predictions["prediction_label"])
