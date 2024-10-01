# s24982.py
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from typing import Tuple, List


class LogisticRegression:
    def __init__(self, learning_rate=0.01, n_iterations=1000) -> None:
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.bias = 0
        self.weights = 0

    def train(self, X, y) -> None:
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iterations):
            dot_prod = np.dot(X, self.weights) + self.bias
            y_pred = self.sigmoid(dot_prod)

            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X) -> List[int]:
        dot_prod = np.dot(X, self.weights) + self.bias
        y_pred = self.sigmoid(dot_prod)
        y_pred_cls = [1 if i > 0.5 else 0 for i in y_pred]
        return y_pred_cls

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))


# Generowanie prostego zbioru danych
def generate_data() -> Tuple[np.ndarray, np.ndarray]:
    X, y = make_blobs(n_features=2, n_samples=100, centers=2, random_state=1337)
    return X, y


# Trenowanie prostego modelu regresji logistycznej
def train_model():
    X, y = generate_data()

    # Podział na zbiór treningowy i testowy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1337)

    # Trenowanie modelu
    logistic_regression = LogisticRegression()
    logistic_regression.train(X_train, y_train)

    # Predykcja na zbiorze testowym
    y_pred = logistic_regression.predict(X_test)

    # Wyliczenie dokładności
    accuracy = np.sum(y_test == y_pred) / len(y_test)

    # Zapis wyniku
    with open("accuracy.txt", "w") as file:
        file.write(f"Model trained with accuracy: {accuracy * 100:.2f}%")

    print(f"Model trained with accuracy: {accuracy * 100:.2f}%")


if __name__ == "__main__":
    train_model()
