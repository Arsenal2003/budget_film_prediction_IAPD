import pandas as pd
import numpy as np

df = pd.read_csv("../data/movies_cleaned_final.csv")
def runtime_to_minutes(x):
    if isinstance(x, str):
        h, m = 0, 0
        if 'h' in x:
            h = int(x.split('h')[0])
            x = x.split('h')[1]
        if 'm' in x:
            m = int(x.replace('m', '').strip())
        return h * 60 + m
    return np.nan

df["Runtime_minutes"] = df["Runtime"].apply(runtime_to_minutes)

df["ROI"] = df["Gross Worldwide"] / df["Budget"]

def first_entity(x):
    if isinstance(x, str):
        return x.split(",")[0].strip()
    return "Unknown"

df["Director_main"] = df["Directors"].apply(first_entity)
df["Writer_main"] = df["Writers"].apply(first_entity)
df["Star_main"] = df["Stars"].apply(first_entity)
df["Genre_main"] = df["Genres"].apply(first_entity)

df = df.drop(columns=["Directors", "Writers", "Stars", "Genres", "Runtime"])

df.to_csv("../data/movies_with_roi_features.csv", index=False)