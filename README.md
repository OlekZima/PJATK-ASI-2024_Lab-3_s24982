# Laboratoirum 4 [ASI]

Continuation on _Laboratorium 3_.

Python app to predict student score based on CollegeDistance dataset.

![Screenshot of the app](assets/screenshot.png)

## How to run

1. [Run Locally](#run-locally)
2. [Run Locally with Docker](#run-locally-with-docker)
3. [Run with Docker Only](#run-with-docker-only)

---

## Run Locally

1. Download git from the [official website](https://git-scm.com/downloads).
   Once downloaded, open your terminal and
   check git's version:
      ```bash
      git --version
      ```
   Example output:
   ```
   git version 2.47.0
   ```
2. Clone this repo by copying/pasting this commands into your terminal:
   ```bash
   git clone https://github.com/OlekZima/PJATK-ASI-2024_Lab-4_s24982
   cd PJATK-ASI-2024_Lab-4_s24982
   ```
3. Install python from the [official website](https://www.python.org/)
   or [conda](https://docs.anaconda.com/miniconda/miniconda-install/).
   Check python's version by this command:
   ```bash
   python --version
   ```
   Example output:
   ```bash
   Python 3.9.20
   ```
4. Install dependencies by running this command:
     ```bash
      python -m pip install requirements.txt
      ```
5. Run the app:
     ```bash
     streamlit run main.py --server.port=8501
     ```
6. Go to http://localhost:8501 to use the app.

---

# Run Locally with Docker

1. Download git from the [official website](https://git-scm.com/downloads).
   Once downloaded, open your terminal and
   check git's version:
   ```bash
   git --version
   ```
   Example output:
   ```
   git version 2.47.0
   ```
2. Clone this repo by copying/pasting this commands into your terminal:
   ```bash
   git clone https://github.com/OlekZima/PJATK-ASI-2024_Lab-4_s24982
   cd PJATK-ASI-2024_Lab-4_s24982
   ```
3. Download docker from the [official website](https://docs.docker.com/get-started/get-docker/).
   Check if the docker works:
   ```bash
   docker run hello-world
   ```
4. Build and run docker image
   ```bash
   docker build score-predictor .
   docker run -p 8501:8501 score-predictor
   ```
5. Go to http://localhost:8501 to use the app.

---

## Run with docker only

1. Download docker from the [official website](https://docs.docker.com/get-started/get-docker/).
   Check if the docker works:
   ```bash
   docker run hello-world
   ```
2. Download docker image:
   ```bash
   docker pull olekzima/score-predictor:latest
   ```
3. Run the image:
   ```bash
   docker run -p 8501:8501 olekzima/score-predictor:latest
   ```
4. Go to http://localhost:8501 to use the app.