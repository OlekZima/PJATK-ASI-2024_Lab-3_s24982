# Laboratoirum 2 [ASI]

## Obróbka danych

### Opis:

Repozytorium pobiera skrypt generujący dane w postaci CSV i wczytuje je do Google Spreadsheet poprzez Google Spreadsheet API.
W tym samym czasie dane są przetwarzane przez klasę `DataPreparator` i zapisywane w pliku `prepared.csv`, który zostaje w artefaktach.
Następnie przetworzone dane są wczytywane do w.w. Google Spreadsheet.

### Generowanie danych:

Dane są pobierane z [tego](https://github.com/PJATK-ASI-2024/Lab2---Obr-bka-danych) repozytorium.

### Google Spreadsheet API:

Połączenie odbywa się za pomocą konta serwisowego, którego JSON znaduje się w sekrecie repozytorium.

### Przetwarzenie danych:

Dane są przetwarzane za pomocą biblioteki `pandas`

### Używanie:
Uruchom po kolei
1. `pip -r install requirements.txt` to install all dependencies.
2. `python generate_upload.py --cred ... --spreadsheet ... --file ...` to generate and upload data to the selected spreadsheet specified by the `--spreadhseet` flag. You need to pass service account credentials json using `--cred`. Service account should have access to the given spreadsheet and you must enable Google Spreadsheet API.
3. `python get_prepare_upload.py --cred ... --spreadsheet ...` to download data from given spreadsheet using given credentials, prepare those data and upload to the second Sheet of the spreadsheet.