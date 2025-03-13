import streamlit as st
import pandas as pd
import datetime
import os

# Configuración inicial
st.set_page_config(page_title="F1 Fantasy", layout="wide")

# Datos de Grandes Premios y Pilotos
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

# Archivos CSV para almacenamiento persistente
PREDICTIONS_FILE = "predictions.csv"
RESULTS_FILE = "results.csv"

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
    
    return {"predictions": predictions, "results": results}

data = load_data()

# Función para registrar una predicción
def save_prediction(jugador, gran_premio, Sesión, p1, p2, p3):
    now = datetime.datetime.now()
    nueva_prediccion = pd.DataFrame({
        "Jugador": [jugador],
        "Gran Premio": [gran_premio],
        "Sesión": [Sesión],
        "P1": [p1],
        "P2": [p2],
        "P3": [p3],
        "Fecha": [now]
    })
    data["predictions"] = pd.concat([data["predictions"], nueva_prediccion], ignore_index=True)
    data["predictions"].to_csv(PREDICTIONS_FILE, index=False)

# Función para ingresar los resultados reales
def save_results(gran_premio, Sesión, p1, p2, p3):
    nuevo_resultado = pd.DataFrame({
        "Gran Premio": [gran_premio],
        "Sesión": [Sesión],
        "P1": [p1],
        "P2": [p2],
        "P3": [p3]
    })
    data["results"] = pd.concat([data["results"], nuevo_resultado], ignore_index=True)
    data["results"].to_csv(RESULTS_FILE, index=False)

# Interfaz de predicción
st.title("🏎️ F1 Fantasy ")
st.subheader("2025")

jugador = st.selectbox("Gambler", ["Maggi", "Pié", "Ric"])
gran_premio = st.selectbox("Gran Premio", list(grandes_premios.keys()))
Sesión = st.radio("Sesión", ["Qualy", "Qualy Sprint", "Sprint", "Carrera"])

if st.checkbox("Ingresar resultados oficiales"):
    st.subheader("Resultados Oficiales")
    p1_res = st.selectbox("P1", pilotos, key="p1_res")
    p2_res = st.selectbox("P2", pilotos, key="p2_res")
    p3_res = st.selectbox("P3", pilotos, key="p3_res")
    if st.button("Guardar Resultados"):
        save_results(gran_premio, Sesión, p1_res, p2_res, p3_res)
        st.success("Resultados guardados correctamente!")

p1 = st.selectbox("P1", pilotos, key="p1_pred")
p2 = st.selectbox("P2", pilotos, key="p2_pred")
p3 = st.selectbox("P3", pilotos, key="p3_pred")

if st.button("Save Prediction"):
    save_prediction(jugador, gran_premio, Sesión, p1, p2, p3)
    st.success("Predicción guardada correctamente!")

# Mostrar tabla de predicciones actuales
st.subheader("📊 Predicciones")
st.dataframe(data["predictions"])

# Mostrar resultados oficiales
st.subheader("🏁 Resultados Oficiales")
st.dataframe(data["results"])
