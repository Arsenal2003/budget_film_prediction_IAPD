import pandas as pd

# Numele fișierelor de intrare
csv1 = "imdb_movies_data.csv"
csv2 = "imdb_movies_data_rev.csv"

# Numele fișierului rezultat
output_csv = "result_data_movies.csv"

# Citim fișierele CSV
df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)

# Concatenăm cele două DataFrame-uri
concat = pd.concat([df1, df2], ignore_index=True)

# Eliminăm duplicatele
fara_duplicate = concat.drop_duplicates()

# Salvăm rezultatul într-un nou fișier CSV
fara_duplicate.to_csv(output_csv, index=False)

print(f"Fișierele '{csv1}' și '{csv2}' au fost concatenate fără duplicate în '{output_csv}'.")