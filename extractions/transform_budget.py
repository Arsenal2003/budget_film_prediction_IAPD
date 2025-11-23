import pandas as pd
import numpy as np
import re

CURRENCY_TO_USD = {
    "$": 1.0,
    "US$": 1.0,
    "USD": 1.0,

    # Euro & pre-Euro
    "€": 1.10,
    "EUR": 1.10,
    "DEM": 1.10 / 1.95583,       # German Mark
    "FRF": 1.10 / 6.55957,       # French Franc
    "ITL": 1.10 / 1936.27,       # Italian Lira
    "ESP": 1.10 / 166.386,       # Spanish Peseta
    "NLG": 1.10 / 2.20371,       # Dutch Guilder
    "BEF": 1.10 / 40.3399,       # Belgian Franc
    "ATS": 1.10 / 13.7603,       # Austrian Schilling
    "FIM": 1.10 / 5.94573,       # Finnish Markka
    "GRD": 1.10 / 340.75 if "GRD" else 0,    # never occurred but included
    
    # Pound
    "£": 1.25,
    "GBP": 1.25,

    # Yen
    "¥": 0.0063,     # Japanese Yen → USD
    "JPY": 0.0063,
    # Yuan
    "CNY": 0.14,     # Chinese Yuan
    "₩": 0.00075,   # South Korean Won
    "KRW": 0.00075,
    # Dollar variants
    "CA$": 0.74,     # Canadian Dollar
    "CAD": 0.74,
    "A$": 0.66,      # Australian Dollar
    "AUD": 0.66,
    "NZ$": 0.60,     # New Zealand Dollar
    "HK$": 0.13,     # Hong Kong Dollar
    "SGD": 0.74,     # Singapore Dollar
    "NT$": 0.031,    # Taiwan Dollar
    "R$": 0.20,     # Brazilian Real

    # Nordic
    "DKK": 0.15,     # Danish Krone
    "NOK": 0.095,    # Norwegian Krone
    "SEK": 0.091,    # Swedish Krona

    # Eastern Europe
    "PLN": 0.25,     # Polish Zloty
    "HUF": 0.0028,   # Hungarian Forint
    "CZK": 0.044,    # Czech Koruna
    "ROL": 0.00022,  # Old Romanian Leu (ROL)

    "LTL": 1.10 / 3.45280,   # Lithuanian Litas → euro → usd

    # Russia
    "RUR": 0.011,    # Russian Ruble (older)
    "RUB": 0.011,

    # Asia
    "THB": 0.028,    # Thai Baht
    "PKR": 0.0036,   # Pakistani Rupee
    "CN": 0.14,      # Chinese Yuan (should be CNY)
    
    # Switzerland
    "CHF": 1.15,     # Swiss Franc

    # Others
    "BND": 0.74,   # Brunei Dollar (pegged to SGD)
    "TRL": 0.000032,  # Old Turkish Lira

    "CN¥": 0.14,  # Chinese Yuan with Yen symbol
    "NZ$": 0.60,     # New Zealand Dollar
    "₹": 0.012,    # Indian Rupee
    "INR": 0.012,
}

# -------------------------------------------------------
# Detectăm orice valută care este în dicționarul tău !
# -------------------------------------------------------
CURRENCY_REGEX = re.compile(
    r"^\s*(" +
    "|".join(
        sorted(
            map(
                re.escape,
                CURRENCY_TO_USD.keys()
            ),
            key=lambda x: -len(x)  # match cel mai lung token întâi
        )
    ) +
    r")\s*",
    flags=re.IGNORECASE
)

def clean_money_column(value):
    if pd.isna(value):
        return np.nan

    v = str(value).strip()

    # scoatem parantezele (estimate), etc
    v = re.sub(r"\(.*?\)", "", v).strip()

    # ----------------------------------------
    # 1. detectăm valuta exact din dicționar
    # ----------------------------------------
    m = CURRENCY_REGEX.match(v)
    if not m:
        return np.nan

    currency = m.group(1)

    # normalizare (atenție: simbolurile rămân exact cum sunt)
    currency = currency.upper()

    # corectăm forme alternative
    replacements = {
        "US$": "USD",
        "CA$": "CA$",
        "AU$": "A$",
        "NZ$": "NZ$",
        "HK$": "HK$"
    }
    currency = replacements.get(currency, currency)

    if currency not in CURRENCY_TO_USD:
        return np.nan

    # ----------------------------------------
    # 2. extragem numărul (perfect tolerant)
    # ----------------------------------------
    number_match = re.search(r"[\d.,]+", v)
    if not number_match:
        return np.nan

    n = number_match.group(0)

    # normalizare universală
    # dacă apare atât punct cât și virgulă -> european
    if "," in n and "." in n:
        n = n.replace(".", "").replace(",", ".")
    # doar virgulă, multe -> separator mii
    elif n.count(",") > 1:
        n = n.replace(",", "")
    # doar punct, multe -> separator mii
    elif n.count(".") > 1:
        n = n.replace(".", "")
    # doar virgula și pare thousand → elimini
    elif "," in n and len(n.split(",")[-1]) == 3:
        n = n.replace(",", "")
    # doar virgula dar nu thousand -> decimal
    else:
        n = n.replace(",", "")

    try:
        number = float(n)
    except:
        return np.nan

    # ----------------------------------------
    # 3. convertește în USD
    # ----------------------------------------
    return number * CURRENCY_TO_USD[currency]



def clean_and_fill(input_file, output_file):
    # Load data
    df = pd.read_csv(input_file)

    # -----------------------------------
    # 0. Popularity → numeric
    # -----------------------------------
    df["Popularity"] = (
        df["Popularity"]
        .astype(str)
        .str.replace(",", "")       # elimină eventuale virgule
        .str.extract(r"(\d+\.?\d*)") # scoate doar numărul
        .astype(float)
    )
    
    # ------------------------------
    # 1. Clean Budget & Gross Worldwide
    # ------------------------------
    df["Budget_cleaned"] = df["Budget"].apply(clean_money_column)
    df["Gross_cleaned"] = df["Gross Worldwide"].apply(clean_money_column)

    # Replace original columns
    df["Budget"] = df["Budget_cleaned"]
    df["Gross Worldwide"] = df["Gross_cleaned"]

    df = df.drop(columns=["Budget_cleaned", "Gross_cleaned"])

    # ------------------------------
    # 2. Fill missing values with mode
    # ------------------------------
    for col in df.columns:
        if df[col].isna().any():
            try:
                mode_value = df[col].mode()[0]
                df[col] = df[col].fillna(mode_value) 
            except:
                pass

    # Save cleaned file
    df.to_csv(output_file, index=False)
    print(f"File cleaned and saved to: {output_file}")


# Example run:
clean_and_fill(
    "../data/result_data_movies.csv",
    "../data/movies_cleaned_final.csv"
)