# proyecto_etl_tenis_2
# Pipeline ETL de Tenis ATP & Cubo Analítico con PySpark 🎾🚀

Este proyecto implementa el ciclo de vida completo del dato en el circuito de tenis profesional masculino (ATP) para el periodo **2015-2023**. Se ha construido un pipeline de datos robusto, modular y reproducible que abarca desde la ingesta de orígenes heterogéneos hasta la explotación analítica distribuida bajo un modelo OLAP.

Desarrollado para la plataforma estadística ficticia **"TennisStats Analytics"** en la asignatura *Introducción a los Sistemas Big Data — Valor de la Información* (Curso 2025-2026).

## 👥 Integrantes del Grupo
* Álvaro Prieto
* Alejandro Rodríguez
* Yago Robles

---

## 📁 Estructura del Repositorio

El proyecto sigue una arquitectura de carpetas estandarizada para garantizar la mantenibilidad y el aislamiento de entornos:

```text
proyecto_etl_tenis_2/
├── data/
│   ├── raw/          # Orígenes de datos brutos (CSV y JSON de rankings)
│   ├── processed/    # Datos intermedios limpios tras la fase de Transformación
│   └── final/        # Tablas definitivas del Modelo en Estrella listas para producción
├── src/
│   ├── extract.py    # Módulo de extracción e ingesta de fuentes
│   ├── transform.py  # Pipeline de limpieza, calidad y lógica de negocio
│   ├── load.py       # Creación del Modelo Dimensional y carga en SQLite
│   └── tracker.py    # Clase de auditoría y tracking del pipeline (logs en JSON)
├── notebooks/
│   └── notebooks_pyspark.ipynb  # Cuaderno analítico OLAP ejecutado en Google Colab
├── logs/
│   └── etl_tracker.json         # Historial detallado de auditoría del pipeline
└── README.md         # Documentación del proyecto

