import streamlit as st
import pandas as pd
import datetime
import os

# Configuración inicial
st.set_page_config(page_title="F1 Fantasy", layout="wide")

# Diccionario actualizado de Grandes Premios con horarios de cada sesión
grandes_premios = {
    "Rolex Australian Grand Prix": {
        "fecha": "2025-03-16",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-03-15 06:00",
            "Carrera": "2025-03-16 05:00"
        }
    },
    "Heineken Chinese Grand Prix": {
        "fecha": "2025-03-23",
        "sprint": True,
        "sesiones": {
            "Qualy Sprint": "2025-03-21 08:30",
            "Sprint": "2025-03-22 04:00",
            "Qualy": "2025-03-22 08:00",
            "Carrera": "2025-03-23 08:00"
        }
    },
    "Honda Japanese Grand Prix": {
        "fecha": "2025-04-06",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-04-05 08:00",
            "Carrera": "2025-04-06 07:00"
        }
    },
    "Gulf Air Bahrain Grand Prix": {
        "fecha": "2025-04-13",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-04-12 18:00",
            "Carrera": "2025-04-13 17:00"
        }
    },
    "STC Saudi Arabian Grand Prix": {
        "fecha": "2025-04-20",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-04-19 19:00",
            "Carrera": "2025-04-20 19:00"
        }
    },
    "Crypto.com Miami Grand Prix": {
        "fecha": "2025-05-04",
        "sprint": True,
        "sesiones": {
            "Qualy Sprint": "2025-05-02 22:30",
            "Sprint": "2025-05-03 18:00",
            "Qualy": "2025-05-03 22:00",
            "Carrera": "2025-05-04 22:00"
        }
    },
    "Qatar Airways Emilia-Romagna Grand Prix": {
        "fecha": "2025-05-18",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-05-17 16:00",
            "Carrera": "2025-05-18 15:00"
        }
    },
    "Monaco Grand Prix": {
        "fecha": "2025-05-25",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-05-24 16:00",
            "Carrera": "2025-05-25 15:00"
        }
    },
    "Pirelli Spanish Grand Prix": {
        "fecha": "2025-06-01",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-05-31 16:00",
            "Carrera": "2025-06-01 15:00"
        }
    },
    "AWS Canadian Grand Prix": {
        "fecha": "2025-06-15",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-06-14 22:00",
            "Carrera": "2025-06-15 20:00"
        }
    },
    "Qatar Airways Austrian Grand Prix": {
        "fecha": "2025-06-29",
        "sprint": True,  # Marcado como True en el código original
        "sesiones": {
            "Qualy": "2025-06-28 16:00",
            "Carrera": "2025-06-29 15:00"
            # No se han proporcionado datos para "Qualy Sprint" o "Sprint"
        }
    },
    "Aramco British Grand Prix": {
        "fecha": "2025-07-06",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-07-05 16:00",
            "Carrera": "2025-07-06 16:00"
        }
    },
    "MSC Cruises Belgian Grand Prix": {
        "fecha": "2025-07-27",
        "sprint": True,
        "sesiones": {
            "Qualy Sprint": "2025-07-25 16:30",
            "Sprint": "2025-07-26 12:00",
            "Qualy": "2025-07-26 16:00",
            "Carrera": "2025-07-27 15:00"
        }
    },
    "Magyar Nagydíj Hungarian Grand Prix": {
        "fecha": "2025-08-03",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-08-02 16:00",
            "Carrera": "2025-08-03 15:00"
        }
    },
    "Heineken Dutch Grand Prix": {
        "fecha": "2025-08-31",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-08-30 15:00",
            "Carrera": "2025-08-31 15:00"
        }
    },
    "Pirelli Italian Grand Prix": {
        "fecha": "2025-09-07",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-09-06 16:00",
            "Carrera": "2025-09-07 15:00"
        }
    },
    "Singapore Airlines Singapore Grand Prix": {
        "fecha": "2025-09-21",  # Mantienes la fecha original
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-10-04 15:00",
            "Carrera": "2025-10-05 14:00"
        }
    },
    "Lenovo United States Grand Prix": {
        "fecha": "2025-10-26",  # Mantienes la fecha original
        "sprint": True,
        "sesiones": {
            "Qualy Sprint": "2025-10-17 23:30",
            "Sprint": "2025-10-18 19:00",
            "Qualy": "2025-10-18 23:00",
            "Carrera": "2025-10-19 21:00"
        }
    },
    "Mexico City Grand Prix": {
        "fecha": "2025-11-02",  # Mantienes la fecha original
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-10-25 23:00",
            "Carrera": "2025-10-26 21:00"
        }
    },
    "Lenovo São Paulo Grand Prix": {
        "fecha": "2025-11-16",  # Mantienes la fecha original
        "sprint": True,
        "sesiones": {
            "Qualy Sprint": "2025-11-07 19:30",
            "Sprint": "2025-11-08 15:00",
            "Qualy": "2025-11-08 19:00",
            "Carrera": "2025-11-09 18:00"
        }
    },
    "Qatar Airways Qatar Grand Prix": {
        "fecha": "2025-11-30",
        "sprint": True,
        "sesiones": {
            "Qualy Sprint": "2025-11-28 18:30",
            "Sprint": "2025-11-29 15:00",
            "Qualy": "2025-11-29 19:00",
            "Carrera": "2025-11-30 17:00"
        }
    },
    "Etihad Airways Abu Dhabi Grand Prix": {
        "fecha": "2025-12-07",
        "sprint": False,
        "sesiones": {
            "Qualy": "2025-12-06 15:00",
            "Carrera": "2025-12-07 14:00"
        }
    }
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
            points = 0
            # 6 puntos si acierta exacto, 2 si el piloto predicho está en otro puesto del top 3
            for i in range(3):
                if pred[f"P{i+1}"] == result[f"P{i+1}"]:
                    points += 6
                elif pred[f"P{i+1}"] in [result["P1"], result["P2"], result["P3"]]:
                    points += 2
            # Bonus 10 si acierta todo el top 3 en orden
            if points == 18:
                points += 10
            
            # Mitad de puntos en Sprint o Qualy Sprint
            if pred["Sesión"] in ["Sprint", "Qualy Sprint"]:
                points /= 2
            
            scores[pred["Jugador"]] = scores.get(pred["Jugador"], 0) + points
    
    return pd.DataFrame(list(scores.items()), columns=["Jugador", "Puntos Totales"])

# Función para guardar una predicción de Gran Premio
def save_prediction(jugador, gran_premio, sesion, p1, p2, p3):
    nueva_prediccion = pd.DataFrame({
        "Jugador": [jugador],
        "Gran Premio": [gran_premio],
        "Sesión": [sesion],
        "P1": [p1],
        "P2": [p2],
        "P3": [p3],
        "Fecha": [datetime.datetime.now()]
    })
    data["predictions"] = pd.concat([data["predictions"], nueva_prediccion], ignore_index=True)
    data["predictions"].to_csv(PREDICTIONS_FILE, index=False)

# Función para guardar una predicción global (Mundial)
def save_global_prediction(jugador, categoria, p1, p2, p3):
    nueva_prediccion_global = pd.DataFrame({
        "Jugador": [jugador],
        "Categoría": [categoria],
        "P1": [p1],
        "P2": [p2],
        "P3": [p3]
    })
    data["global_predictions"] = pd.concat([data["global_predictions"], nueva_prediccion_global], ignore_index=True)
    data["global_predictions"].to_csv(GLOBAL_PREDICTIONS_FILE, index=False)

# Interfaz principal
st.title("🏎️ F1 Fantasy 2025")
menu = st.sidebar.radio("Panel", ["Grandes Premios", "Mundial", "Resultados y Puntos"])

if menu == "Grandes Premios":
    st.subheader("Grand Prix weekend")
    
    # Seleccionar jugador y GP
    jugador = st.selectbox("Gambler", ["Maggi", "Pié", "Ric"])
    gran_premio = st.selectbox("Gran Premio", list(grandes_premios.keys()))
    
    # Obtenemos las sesiones reales definidas en el diccionario para ese GP
    sesiones_disponibles = list(grandes_premios[gran_premio]["sesiones"].keys())
    # Escogemos la sesión de entre las disponibles
    sesion = st.radio("Sesión", sesiones_disponibles)
    
    # Determinar si la sesión está abierta o no (en función de la hora actual)
    session_str = grandes_premios[gran_premio]["sesiones"][sesion]
    session_datetime = datetime.datetime.strptime(session_str, "%Y-%m-%d %H:%M")
    session_abierta = datetime.datetime.now() < session_datetime
    
    # Deshabilitar la entrada si la sesión ya comenzó
    p1 = st.selectbox("P1", pilotos, disabled=not session_abierta)
    p2 = st.selectbox("P2", pilotos, disabled=not session_abierta)
    p3 = st.selectbox("P3", pilotos, disabled=not session_abierta)
    
    if st.button("GUARDAR", disabled=not session_abierta):
        save_prediction(jugador, gran_premio, sesion, p1, p2, p3)
        st.success("Predicción guardada")
    
    st.subheader("📊 Predicciones de Gran Premio")
    st.dataframe(data["predictions"])

elif menu == "Mundial":
    st.subheader("F1 World Championship")
    jugador = st.selectbox("Gambler", ["Maggi", "Pié", "Ric"], key="global_jugador")
    categoria = st.radio("Categoría", ["World Drivers Championship", "World Constructors Championship"], key="global_categoria")
    
    if categoria == "World Drivers Championship":
        p1 = st.selectbox("P1", pilotos, key="global_p1")
        p2 = st.selectbox("P2", pilotos, key="global_p2")
        p3 = st.selectbox("P3", pilotos, key="global_p3")
    else:
        p1 = st.selectbox("P1", equipos, key="global_p1")
        p2 = st.selectbox("P2", equipos, key="global_p2")
        p3 = st.selectbox("P3", equipos, key="global_p3")
    
    if st.button("GUARDAR", key="global_guardar"):
        save_global_prediction(jugador, categoria, p1, p2, p3)
        st.success("Predicción global guardada")
    
    st.subheader("📊 Mundial")
    st.dataframe(data["global_predictions"])

elif menu == "Resultados y Puntos":
    st.subheader("Introducir Resultados Reales")
    result_gran_premio = st.selectbox("Gran Premio", list(grandes_premios.keys()), key="result_gp")
    # Para los resultados, también podemos basarnos en las sesiones definidas en el diccionario
    result_sesiones_disponibles = list(grandes_premios[result_gran_premio]["sesiones"].keys())
    result_sesion = st.radio("Sesión", result_sesiones_disponibles, key="result_sesion")
    
    result_p1 = st.selectbox("P1", pilotos, key="result_p1")
    result_p2 = st.selectbox("P2", pilotos, key="result_p2")
    result_p3 = st.selectbox("P3", pilotos, key="result_p3")
    
    if st.button("GUARDAR RESULTADOS", key="guardar_resultados"):
        nueva_resultado = pd.DataFrame({
            "Gran Premio": [result_gran_premio],
            "Sesión": [result_sesion],
            "P1": [result_p1],
            "P2": [result_p2],
            "P3": [result_p3]
        })
        data["results"] = pd.concat([data["results"], nueva_resultado], ignore_index=True)
        data["results"].to_csv(RESULTS_FILE, index=False)
        st.success("Resultados guardados")
    
    st.subheader("📊 Clasificación")
    scores_df = calculate_scores()
    scores_df.to_csv(SCORES_FILE, index=False)
    st.dataframe(scores_df)
