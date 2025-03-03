import streamlit as st
import pandas as pd
import datetime

# Configuración inicial
st.set_page_config(page_title="F1 Fantasy", layout="wide")

# Datos de Grandes Premios y Pilotos
grandes_premios = {
    "Australia": {"fecha": "2025-03-16", "sprint": False},
    "China": {"fecha": "2025-03-23", "sprint": True},
    "Japón": {"fecha": "2025-04-06", "sprint": False},
    "Bahréin": {"fecha": "2025-04-13", "sprint": False},
    "Arabia Saudí": {"fecha": "2025-04-20", "sprint": False},
    "Miami": {"fecha": "2025-05-04", "sprint": True},
    "Italia (Imola)": {"fecha": "2025-05-18", "sprint": False},
    "Mónaco": {"fecha": "2025-05-25", "sprint": False},
    "España": {"fecha": "2025-06-01", "sprint": False},
    "Canadá": {"fecha": "2025-06-15", "sprint": False},
    "Austria": {"fecha": "2025-06-29", "sprint": True},
    "Reino Unido": {"fecha": "2025-07-06", "sprint": False},
    "Bélgica": {"fecha": "2025-07-27", "sprint": True},
    "Hungría": {"fecha": "2025-08-03", "sprint": False},
    "Países Bajos": {"fecha": "2025-08-31", "sprint": False},
    "Italia (Monza)": {"fecha": "2025-09-07", "sprint": False},
    "Singapur": {"fecha": "2025-09-21", "sprint": False},
    "Japón": {"fecha": "2025-10-12", "sprint": False},
    "Estados Unidos (Austin)": {"fecha": "2025-10-26", "sprint": True},
    "México": {"fecha": "2025-11-02", "sprint": False},
    "Brasil": {"fecha": "2025-11-16", "sprint": True},
    "Qatar": {"fecha": "2025-11-30", "sprint": True},
    "Abu Dhabi": {"fecha": "2025-12-07", "sprint": False}
}

pilotos = [
    "Max Verstappen", "Lando Norris", "Gabriel Bortoleto", "Isack Hadjar", "Jack Doohan",
    "Pierre Gasly", "Andrea Kimi Antonelli", "Fernando Alonso", "Charles Leclerc", "Lewis Hamilton",
    "Liam Lawson", "George Russell", "Oscar Piastri", "Lance Stroll", "Yuki Tsunoda",
    "Alexander Albon", "Nico Hülkenberg", "Esteban Ocon", "Oliver Bearman", "Carlos Sainz", "Franco Colapinto"
]

# Cargar o inicializar datos
@st.cache(allow_output_mutation=True)
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
st.title("🏎️ F1 Fantasy Predictor")
st.subheader("Registra tu predicción para la próxima sesión")

jugador = st.selectbox("Selecciona tu nombre", ["Maggi", "Pié", "Ric"])
gran_premio = st.selectbox("Selecciona el Gran Premio", list(grandes_premios.keys()))
tipo = st.radio("Tipo de sesión", ["Clasificación", "Clasificación Sprint", "Sprint", "Carrera"])

# Verificar si el GP seleccionado tiene sprint
disabled_sprint = tipo in ["Clasificación Sprint", "Sprint"] and not grandes_premios[gran_premio]["sprint"]
if disabled_sprint:
    st.warning(f"El Gran Premio de {gran_premio} no tiene sesión de {tipo}. Por favor, selecciona otro tipo de sesión.")
else:
    p1 = st.selectbox("Piloto en P1", pilotos)
    p2 = st.selectbox("Piloto en P2", pilotos, index=1)
    p3 = st.selectbox("Piloto en P3", pilotos, index=2)

    if st.button("Guardar Predicción"):
        save_prediction(jugador, gran_premio, tipo, p1, p2, p3)
        st.success("Predicción guardada con éxito!")

# Mostrar tabla de predicciones actuales
st.subheader("📊 Predicciones registradas")
st.dataframe(data["predictions"])
