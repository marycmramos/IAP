import os
import pandas as pd

DIRECTORY = r'C:\Users\ASUS\Desktop\3.º ano\2.º  semestre\IAP\proj\matches'
file_list = [f for f in os.listdir(DIRECTORY) if f.endswith('.csv')]

COLUMNS = {
    'Date': 'date',
    'HomeTeam': 'ht',
    'AwayTeam': 'at',
    'FTHG': 'hg',
    'FTAG': 'ag',
    'FTR': 'result',
    'B365H': 'h_odds',
    'B365D': 'd_odds',
    'B365A': 'a_odds',
}

BAD_TEAM_NAMES = {
    'sp lisbon': 'sporting',
    'estrela': 'est amadora',
    'feirense ': 'feirense',
}

match_data_l = []

for file_name in file_list:
    print(file_name)

    path = os.path.join(DIRECTORY, file_name)
    df = pd.read_csv(path, on_bad_lines='warn')

    if not all(col in df.columns for col in COLUMNS):
        print(f"Skipping {file_name} (missing columns)")
        continue

    df = df[[*COLUMNS]]

    df = df.rename(columns=COLUMNS)

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')

    df['ht'] = df['ht'].str.lower()
    df['at'] = df['at'].str.lower()

    df['ht'] = df['ht'].replace(BAD_TEAM_NAMES)
    df['at'] = df['at'].replace(BAD_TEAM_NAMES)

    df = df.dropna()

    df['hg'] = df['hg'].astype(int)
    df['ag'] = df['ag'].astype(int)

    match_data_l.append(df)

matches = pd.concat(match_data_l).sort_values('date').reset_index(drop=True)

matches.to_csv(r'C:\Users\ASUS\Desktop\3.º ano\2.º  semestre\IAP\proj\1_load_dataset.csv', index=False)
