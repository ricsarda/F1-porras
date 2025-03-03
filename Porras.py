import streamlit as st
import pandas as pd
import datetime

# Configuración inicial
st.set_page_config(page_title="F1 Fantasy", layout="wide")

# Cargar o inicializar datos
@st.cache(allow_output_mutation=True)
def load_data():
    return {"predictions": pd.DataFrame(columns=["Jugador", "Tipo", "P1", "P2", "P3", "Fecha"]),
            "scores": pd.DataFrame(columns=["Jugador", "Puntos Totales"])}

data = load_data()

# Función para registrar una predicción
def save_prediction(jugador, tipo, p1, p2, p3):
    now = datetime.datetime.now()
    nueva_prediccion = pd.DataFrame({
        "Jugador": [jugador],
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

jugador = st.selectbox("Selecciona tu nombre", ["Jugador 1", "Jugador 2", "Jugador 3"])
tipo = st.radio("Tipo de sesión", ["Clasificación", "Sprint", "Carrera"])
p1 = st.text_input("Piloto en P1")
p2 = st.text_input("Piloto en P2")
p3 = st.text_input("Piloto en P3")

if st.button("Guardar Predicción"):
    save_prediction(jugador, tipo, p1, p2, p3)
    st.success("Predicción guardada con éxito!")

# Mostrar tabla de predicciones actuales
st.subheader("📊 Predicciones registradas")
st.dataframe(data["predictions"])

# Placeholder para futuras funcionalidades: cálculo de puntuaciones y bloqueos de tiempo
