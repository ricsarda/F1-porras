import streamlit as st
import pandas as pd
import datetime
import os

# Configuración inicial
st.set_page_config(page_title="F1 Fantasy", layout="wide")

# Datos de Grandes Premios, Pilotos y Equipos
grandes_premios = {
    "Rolex Australian Grand Prix": {"fecha": "2025-03-16", "sprint": False},
    "Heineken Chinese Grand Prix": {"fecha": "2025-03-23", "sprint": True},
    "Honda Japanese Grand Prix": {"fecha": "2025-04-06", "sprint": False},
    "Gulf Air Bahrain Grand Prix": {"fecha": "2025-04-13", "sprint": False},
    "STC Saudi Arabian Grand Prix": {"fecha": "2025-04-20", "sprint": False},
    "Crypto.com Miami Grand Prix": {"fecha": "2025-05-04", "sprint": True},
    "Qatar Airways Emilia-Romagna Grand Prix": {"fecha": "2025-05-18", "sprint": False},
    "Monaco Grand Prix": {"fecha": "2025-05-25", "sprint": False},
    "Pirelli Spanish Grand Prix": {"fecha": "2025-06-01", "sprint": False},
    "AWS Canadian Grand Prix": {"fecha": "2025-06-15", "sprint": False},
    "Qatar Airways Austrian Grand Prix": {"fecha": "2025-06-29", "sprint": True},
    "Aramco British Grand Prix": {"fecha": "2025-07-06", "sprint": False},
    "MSC Cruises Belgian Grand Prix": {"fecha": "2025-07-27", "sprint": True},
    "Magyar Nagydíj Hungarian Grand Prix": {"fecha": "2025-08-03", "sprint": False},
    "Heineken Dutch Grand Prix": {"fecha": "2025-08-31", "sprint": False},
    "Pirelli Italian Grand Prix": {"fecha": "2025-09-07", "sprint": False},
    "Singapore Airlines Singapore Grand Prix": {"fecha": "2025-09-21", "sprint": False},
    "Lenovo United States Grand Prix": {"fecha": "2025-10-26", "sprint": True},
    "Mexico City Grand Prix": {"fecha": "2025-11-02", "sprint": False},
    "Lenovo São Paulo Grand Prix": {"fecha": "2025-11-16", "sprint": True},
    "Qatar Airways Qatar Grand Prix": {"fecha": "2025-11-30", "sprint": True},
    "Etihad Airways Abu Dhabi Grand Prix": {"fecha": "2025-12-07", "sprint": False}
}

pilotos = [
    "Max Verstappen", "Lando Norris", "Gabriel Bortoleto", "Isack Hadjar", "Jack Doohan",
    "Pierre Gasly", "Andrea Kimi Antonelli", "Fernando Alonso", "Charles Leclerc", "Lewis Hamilton",
    "Liam Lawson", "George Russell", "Oscar Piastri", "Lance Stroll", "Yuki Tsunoda",
    "Alexander Albon", "Nico Hülkenberg", "Esteban Ocon", "Oliver Bearman", "Carlos Sainz", "Franco Colapinto"
]

equipos = [
    "Red Bull Racing", "Ferrari", "Mercedes", "McLaren", "Aston Martin",
    "Alpine", "Haas", "Williams", "RB", "Sauber"
]

# Archivos CSV para almacenamiento persistente
PREDICTIONS_FILE = "predictions.csv"
RESULTS_FILE = "results.csv"
GLOBAL_PREDICTIONS_FILE = "global_predictions.csv"
SCORES_FILE = "scores.csv"

# Cargar o inicializar datos
def load_data():
    if os.path.exists(PREDICTIONS_FILE):
        predictions = pd.read_csv(PREDICTIONS_FILE)
    else:
        predictions = pd.DataFrame(columns=["Jugador", "Gran Premio", "Sesión", "P1", "P2", "P3", "Fecha"])
    
    if os.path.exists(RESULTS_FILE):
        results = pd.read_csv(RESULTS_FILE)
    else:
        results = pd.DataFrame(columns=["Gran Premio", "Sesión", "P1", "P2", "P3"])
    
    if os.path.exists(GLOBAL_PREDICTIONS_FILE):
        global_predictions = pd.read_csv(GLOBAL_PREDICTIONS_FILE)
    else:
        global_predictions = pd.DataFrame(columns=["Jugador", "Categoría", "P1", "P2", "P3"])
    
    return {"predictions": predictions, "results": results, "global_predictions": global_predictions}

data = load_data()

# Función para calcular puntuaciones automáticamente
def calculate_scores():
    scores = {}
    for _, pred in data["predictions"].iterrows():
        result = data["results"][
            (data["results"]["Gran Premio"] == pred["Gran Premio"]) & (data["results"]["Sesión"] == pred["Sesión"])
        ]
        if not result.empty:
            result = result.iloc[0]
            points = sum([6 if pred[f"P{i+1}"] == result[f"P{i+1}"] else (2 if pred[f"P{i+1}"] in result.values else 0) for i in range(3)])
            if points == 18:
                points += 10  # Bonus por acertar todo
            if pred["Sesión"] == "Sprint":
                points /= 2
            scores[pred["Jugador"]] = scores.get(pred["Jugador"], 0) + points
    return pd.DataFrame(list(scores.items()), columns=["Jugador", "Puntos Totales"])

# Interfaz principal
st.title("🏎️ F1 Fantasy 2025")
menu = st.sidebar.radio("Panel", ["Grandes Premios", "Mundial", "Resultados y Puntos"])

if menu == "Grandes Premios":
    st.subheader("Grand Prix weekend")
    jugador = st.selectbox("Gambler", ["Maggi", "Pié", "Ric"])
    gran_premio = st.selectbox("Gran Premio", list(grandes_premios.keys()))
    sesion = st.radio("Sesión", ["Qualy", "Qualy Sprint", "Sprint", "Carrera"])
    
    p1 = st.selectbox("P1", pilotos)
    p2 = st.selectbox("P2", pilotos)
    p3 = st.selectbox("P3", pilotos)
    
    if st.button("GUARDAR"):
        save_prediction(jugador, gran_premio, sesion, p1, p2, p3)
        st.success("Guardado")
    
    st.subheader("📊 Predicciones de Gran Premio")
    st.dataframe(data["predictions"])

elif menu == "Mundial":
    st.subheader("F1 World Championship")
    jugador = st.selectbox("Gambler", ["Maggi", "Pié", "Ric"], key="global_jugador")
    categoria = st.radio("Categoría", ["World Drivers Championships", "World Constructors Championshipp"], key="global_categoria")
    
    if categoria == "World Drivers Championship":
        p1 = st.selectbox("P1", pilotos, key="global_p1")
        p2 = st.selectbox("P2", pilotos, key="global_p2")
        p3 = st.selectbox("P3", pilotos, key="global_p3")
    else:
        p1 = st.selectbox("P1", equipos, key="global_p1")
        p2 = st.selectbox("P2", equipos, key="global_p2")
        p3 = st.selectbox("P3", equipos, key="global_p3")
    
    if st.button("GUARDAR"):
        save_global_prediction(jugador, categoria, p1, p2, p3)
        st.success("Guardado")
    
    st.subheader("📊 Mundial")
    st.dataframe(data["global_predictions"])

elif menu == "Resultados y Puntos":
    st.subheader("📊 Clasificación")
    scores_df = calculate_scores()
    scores_df.to_csv(SCORES_FILE, index=False)
    st.dataframe(scores_df)
