import streamlit as st
import pandas as pd
import datetime

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

# Cargar o inicializar datos
@st.cache_data
def load_data():
    return {"predictions": pd.DataFrame(columns=["Jugador", "Gran Premio", "Tipo", "P1", "P2", "P3", "Fecha"]),
            "scores": pd.DataFrame(columns=["Jugador", "Puntos Totales"])}

data = load_data()

# Función para registrar una predicción
def save_prediction(jugador, gran_premio, tipo, p1, p2, p3):
    now = datetime.datetime.now()
    nueva_prediccion = pd.DataFrame({
        "Jugador": [jugador],
        "Gran Premio": [gran_premio],
        "Tipo": [tipo],
        "P1": [p1],
        "P2": [p2],
        "P3": [p3],
        "Fecha": [now]
    })
    data["predictions"] = pd.concat([data["predictions"], nueva_prediccion], ignore_index=True)

# Interfaz de predicción
st.title("🏎️ F1 Fantasy ")
st.subheader("2025")

jugador = st.selectbox("Gambler", ["Maggi", "Pié", "Ric"])
gran_premio = st.selectbox("Gran Premio", list(grandes_premios.keys()))
tipo = st.radio("Sesión", ["Clasificación", "Clasificación Sprint", "Sprint", "Carrera"])

# Verificar si el GP seleccionado tiene sprint
disabled_sprint = tipo in ["Clasificación Sprint", "Sprint"] and not grandes_premios[gran_premio]["sprint"]
if disabled_sprint:
    st.warning(f"El Gran Premio de {gran_premio} no tiene sesión de {tipo} tontito")
else:
    p1 = st.selectbox("P1", pilotos)
    p2 = st.selectbox("P2", pilotos, index=1)
    p3 = st.selectbox("P3", pilotos, index=2)

    if st.button("Save"):
        save_prediction(jugador, gran_premio, tipo, p1, p2, p3)
        st.success("Ufff")

# Mostrar tabla de predicciones actuales
st.subheader("📊 Clasificación")
st.dataframe(data["predictions"])
