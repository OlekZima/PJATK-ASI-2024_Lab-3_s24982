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

### Przetworzenie danych:

Dane są przetwarzane za pomocą biblioteki `pandas`