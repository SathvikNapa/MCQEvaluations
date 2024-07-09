import pandas as pd


def handle_csv(file_path: str):
    csv_df = pd.read_csv(file_path)
