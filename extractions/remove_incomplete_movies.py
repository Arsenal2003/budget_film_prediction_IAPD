import pandas as pd

def clean_drop_missing(input_file, output_file):
    df = pd.read_csv(input_file)
    df_clean = df.dropna()
    df_clean.to_csv(output_file, index=False)
    print(f"Fișier curățat salvat ca: {output_file}")

clean_drop_missing("../data/result_data_movies.csv", "../data/only_completed_movies.csv")