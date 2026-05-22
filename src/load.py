import pandas as pd
import os
from sqlalchemy import create_engine, text

# 1. Crear la base de datos SQLite
engine = create_engine("sqlite:///tenis_dw.db")

# 2. Leer los datos limpios
df_matches = pd.read_csv("data/processed/partidos_clean.csv", low_memory=False)
df_players = pd.read_csv("data/processed/jugadores_clean.csv", low_memory=False)

df_matches['tourney_date_dt'] = pd.to_datetime(df_matches['tourney_date'].astype(str), format='%Y%m%d', errors='coerce')

print("Construyendo Modelo en Estrella...")

# --- CREAR DIMENSIONES BÁSICAS ---
dim_jugador = df_players[['player_id', 'name_first', 'name_last', 'hand', 'ioc']].copy()
dim_jugador.insert(0, 'sk_jugador', range(1, 1 + len(dim_jugador)))

superficies = df_matches['surface'].dropna().unique()
dim_superficie = pd.DataFrame({'superficie': superficies})
dim_superficie.insert(0, 'sk_superficie', range(1, 1 + len(dim_superficie)))

fechas = df_matches['tourney_date_dt'].dropna().unique()
dim_tiempo = pd.DataFrame({'fecha': fechas})
dim_tiempo.insert(0, 'sk_tiempo', range(1, 1 + len(dim_tiempo)))
dim_tiempo['anio'] = pd.to_datetime(dim_tiempo['fecha']).dt.year
dim_tiempo['mes'] = pd.to_datetime(dim_tiempo['fecha']).dt.month

torneos = df_matches[['tourney_id', 'tourney_name', 'tourney_level']].drop_duplicates()
dim_torneo = torneos.copy()
dim_torneo.insert(0, 'sk_torneo', range(1, 1 + len(dim_torneo)))

# --- CREAR TABLA DE HECHOS ---
fact = df_matches.merge(dim_tiempo, left_on='tourney_date_dt', right_on='fecha', how='left')
fact = fact.merge(dim_superficie, left_on='surface', right_on='superficie', how='left')
fact = fact.merge(dim_torneo, on='tourney_id', how='left')

dim_jugador['player_id'] = dim_jugador['player_id'].astype(str)
fact['winner_id'] = fact['winner_id'].astype(str)
fact['loser_id'] = fact['loser_id'].astype(str)

fact = fact.merge(dim_jugador[['sk_jugador', 'player_id']], left_on='winner_id', right_on='player_id', how='left').rename(columns={'sk_jugador': 'sk_jugador_gan'})
fact = fact.merge(dim_jugador[['sk_jugador', 'player_id']], left_on='loser_id', right_on='player_id', how='left').rename(columns={'sk_jugador': 'sk_jugador_per'})

fact_partidos = fact[['sk_tiempo', 'sk_superficie', 'sk_torneo', 'sk_jugador_gan', 'sk_jugador_per', 'minutes', 'w_ace', 'l_ace', 'winner_rank', 'loser_rank']].copy()
fact_partidos.insert(0, 'sk_partido', range(1, 1 + len(fact_partidos)))

# 3. Exportar los CSV definitivos
os.makedirs("data/final", exist_ok=True)
dim_jugador.to_csv("data/final/dim_jugador.csv", index=False)
dim_superficie.to_csv("data/final/dim_superficie.csv", index=False)
dim_tiempo.to_csv("data/final/dim_tiempo.csv", index=False)
dim_torneo.to_csv("data/final/dim_torneo.csv", index=False)
fact_partidos.to_csv("data/final/fact_partidos.csv", index=False)
print("CSV Exportados correctamente a la carpeta data/final/")

# 4. Cargar a SQLite
dim_tiempo.to_sql('dim_tiempo', con=engine, if_exists='replace', index=False)
dim_jugador.to_sql('dim_jugador', con=engine, if_exists='replace', index=False)
dim_superficie.to_sql('dim_superficie', con=engine, if_exists='replace', index=False)
dim_torneo.to_sql('dim_torneo', con=engine, if_exists='replace', index=False)
fact_partidos.to_sql('fact_partidos', con=engine, if_exists='replace', index=False)

# 5. Verificación COUNT(*)
with engine.connect() as conn:
    print("\n--- VERIFICACIÓN EN BASE DE DATOS SQLITE ---")
    for tabla in ['dim_tiempo', 'dim_jugador', 'dim_superficie', 'dim_torneo', 'fact_partidos']:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {tabla}")).scalar()
        print(f"Registros en {tabla}: {count}")
