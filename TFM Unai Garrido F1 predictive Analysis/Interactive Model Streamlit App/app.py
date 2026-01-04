import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Cargar modelo y preprocesamiento
model = pickle.load(open("model_pitstop.pkl", "rb"))
scaler = pickle.load(open("scaler_pitstop.pkl", "rb"))
label_encoders = pickle.load(open("label_encoders_pitstop.pkl", "rb"))
features = pickle.load(open("features_pitstop.pkl", "rb"))

st.title("Predicción de Pit Stop en la Próxima Vuelta")

# Interfaz de usuario
input_data = {}
for feature in features:
    if feature in label_encoders:
        options = label_encoders[feature].classes_
        input_data[feature] = st.selectbox(feature, options)
    else:
        input_data[feature] = st.number_input(feature, value=0.0)

if st.button("Predecir"):
    df_input = pd.DataFrame([input_data])

    # Codificar categóricas
    for col in label_encoders:
        df_input[col] = label_encoders[col].transform(df_input[col])

    # Asegurar el orden de columnas
    df_input = df_input[features]

    # Escalar numéricas
    numerical_cols = df_input.select_dtypes(include=["float64", "int64"]).columns.difference(label_encoders.keys())
    df_input[numerical_cols] = scaler.transform(df_input[numerical_cols])

    # Predicción
    pred = model.predict(df_input)[0]
    prob = model.predict_proba(df_input)[0][1]

    st.subheader("Resultado:")
    st.write("🚨 Hará pit stop en la próxima vuelta" if pred == 1 else "✅ No hará pit stop")
    st.write(f"Probabilidad: {prob:.2%}")
