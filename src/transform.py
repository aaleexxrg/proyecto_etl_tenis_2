import pandas as pd
import hashlib
import numpy as np
import os
from tracker import registrar_tracking

def sha256_hash(texto):
    return hashlib.sha256(str(texto).encode('utf-8')).hexdigest()

# Rutas corregidas
df_players = pd.read_csv("data/raw/f2_players.csv")
df_matches = pd.read_csv("data/raw/f1_matches.csv")

regs_antes = len(df_players)
df_players = df_players.drop_duplicates(subset=['player_id'])
registrar_tracking("T01", "F2 Jugadores", regs_antes, len(df_players), regs_antes - len(df_players), "Duplicados por player_id")

df_players['name_first'] = df_players['name_first'].apply(sha256_hash)
df_players['name_last'] = df_players['name_last'].apply(sha256_hash)

df_players['player_id'] = df_players['player_id'].astype(str)
df_matches['winner_id'] = df_matches['winner_id'].astype(str)
df_matches['loser_id'] = df_matches['loser_id'].astype(str)

# Rutas corregidas
os.makedirs("data/processed", exist_ok=True)
df_players.to_csv("data/processed/jugadores_clean.csv", index=False)
df_matches.to_csv("data/processed/partidos_clean.csv", index=False)
