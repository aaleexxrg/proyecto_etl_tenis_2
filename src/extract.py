import pandas as pd
import os
import ssl
from tracker import registrar_tracking

# Esta es la magia que soluciona el error del Mac
ssl._create_default_https_context = ssl._create_unverified_context

URL_MATCHES = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2023.csv"
URL_PLAYERS = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_players.csv"
URL_RANKINGS = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_rankings_current.csv"

os.makedirs("data/raw", exist_ok=True)

df_matches = pd.read_csv(URL_MATCHES)
df_matches.to_csv("data/raw/f1_matches.csv", index=False)
registrar_tracking("EXTRACT", "F1 - Partidos ATP", 0, len(df_matches), 0, "Descarga CSV")

df_players = pd.read_csv(URL_PLAYERS)
df_players.to_csv("data/raw/f2_players.csv", index=False)
registrar_tracking("EXTRACT", "F2 - Jugadores ATP", 0, len(df_players), 0, "Descarga CSV")

df_rankings = pd.read_csv(URL_RANKINGS)
df_rankings.to_json("data/raw/f3_rankings_atp_raw.json", orient="records", indent=2)
registrar_tracking("EXTRACT", "F3 - Rankings ATP", 0, len(df_rankings), 0, "Conversión CSV a JSON")
