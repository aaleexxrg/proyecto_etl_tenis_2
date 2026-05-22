import pandas as pd
import os

def analizar_calidad(df, nombre_fuente):
    print(f"--- PERFIL DE CALIDAD: {nombre_fuente} ---")
    
import pandas as pd
import os

def analizar_calidad(df, nombre_fuente):
    print(f"--- PERFIL DE CALIDAD: {nombre_fuente} ---")
    num_registros = df.shape[0]
    num_variables = df.shape[1]
    print(f"Registros: {num_registros} | Variables: {num_variables}")
    
    nulos_totales = df.isnull().sum().sum()
    porcentaje_nulos = (nulos_totales / (num_registros * num_variables)) * 100
    print(f"Nulos totales: {nulos_totales} ({porcentaje_nulos:.2f}%)")
    
    duplicados = df.duplicated().sum()
    print(f"Duplicados exactos: {duplicados}\n" + "-" * 40)

def ejecutar_limpieza_inicial():
    # Rutas corregidas
    ruta_f1 = "data/raw/f1_matches.csv"
    ruta_f2 = "data/raw/f2_players.csv"
    ruta_f3 = "data/raw/f3_rankings_atp_raw.json"

    if os.path.exists(ruta_f1): analizar_calidad(pd.read_csv(ruta_f1, low_memory=False), "F1 - Partidos ATP")
    else: print("No se encuentra F1.")

    if os.path.exists(ruta_f2): analizar_calidad(pd.read_csv(ruta_f2, low_memory=False), "F2 - Jugadores ATP")
    else: print("No se encuentra F2.")

    if os.path.exists(ruta_f3): analizar_calidad(pd.read_json(ruta_f3), "F3 - Rankings ATP")
    else: print("No se encuentra F3.")

if __name__ == "__main__":
    print("Iniciando análisis de calidad...\n")
    ejecutar_limpieza_inicial()
