import streamlit as st
import numpy as np
import tensorflow as tf
import joblib

# ------------------------
# Cargar modelos y objetos
# ------------------------
model_rank = tf.keras.models.load_model("model_rank.h5")
model_pit = tf.keras.models.load_model("model_pit.h5")

scaler = joblib.load("scaler.pkl")
enc_driver = joblib.load("enc_driver.pkl")
enc_team = joblib.load("enc_team.pkl")
enc_compound = joblib.load("enc_compound.pkl")

# ------------------------
# Configuración básica
# ------------------------
st.set_page_config(page_title="F1 Strategy Predictor", page_icon="🏎️")
st.title("🏁 Estrategia Predictiva en Fórmula 1")
st.markdown("Simula condiciones de carrera para predecir la **posición final** de un piloto y la **probabilidad de hacer un pitstop**.")

# ------------------------
# Formulario de entrada
# ------------------------
with st.form("input_form"):
    st.subheader("📥 Parámetros de carrera")

    col1, col2 = st.columns(2)

    with col1:
        driver = st.selectbox("Piloto", enc_driver.classes_)
        team = st.selectbox("Equipo", enc_team.classes_)
        compound = st.selectbox("Compuesto", enc_compound.classes_)
        fresh_tyre = st.radio("¿Neumático nuevo?", ["Sí", "No"])
        stint = st.slider("Stint actual", 1, 4, 1)
        tyre_life = st.slider("Vueltas con este neumático", 1, 30, 10)

    with col2:
        lap_number = st.slider("Vuelta actual", 1, 70, 10)
        air_temp = st.number_input("🌡️ Temperatura del aire (°C)", value=25.0)
        track_temp = st.number_input("🔥 Temperatura de pista (°C)", value=35.0)
        humidity = st.number_input("💧 Humedad (%)", value=50.0)
        pressure = st.number_input("Presión atmosférica (hPa)", value=1010.0)
        wind_speed = st.number_input("🌬️ Velocidad del viento (km/h)", value=4.0)

    submitted = st.form_submit_button("🔎 Predecir estrategia")

# ------------------------
# Lógica de predicción
# ------------------------
if submitted:
    # Codificar entradas categóricas
    driver_enc = enc_driver.transform([driver])[0]
    team_enc = enc_team.transform([team])[0]
    compound_enc = enc_compound.transform([compound])[0]
    fresh_tyre_binary = 1 if fresh_tyre == "Sí" else 0

    # Variables numéricas
    input_num = np.array([[lap_number, tyre_life, fresh_tyre_binary, stint,
                           air_temp, humidity, pressure, track_temp, wind_speed]])
    input_num_scaled = scaler.transform(input_num)

    # Formato de entrada para los modelos
    inputs = {
        "Driver_input": np.array([driver_enc]),
        "Team_input": np.array([team_enc]),
        "Compound_input": np.array([compound_enc]),
        "numeric_input": input_num_scaled
    }

    # ------------------------
    # Predicción de posición
    # ------------------------
    pred_position = model_rank.predict(inputs)[0][0]
    st.success(f"📍 Posición estimada: **P{pred_position:.2f}**")

    # ------------------------
    # Predicción de pitstop
    # ------------------------
    pit_prob = model_pit.predict(inputs)[0][0]
    st.info(f"🛑 Probabilidad de pitstop en esta vuelta: **{pit_prob * 100:.1f}%**")

    # ------------------------
    # Visual extra
    # ------------------------
    st.subheader("📊 Visualización")
    st.progress(min(pit_prob, 1.0))  # barra de probabilidad de pitstop

    if pit_prob > 0.7:
        st.warning("⚠️ Alta probabilidad de que el piloto pare esta vuelta.")
    elif pit_prob > 0.4:
        st.write("🔄 Posible ventana de parada.")
    else:
        st.success("✅ Poco probable que haya pitstop ahora.")
