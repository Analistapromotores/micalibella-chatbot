# app.py
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="MICALIBELLA", layout="centered")

st.title("🐦 MICALIBELLA: Chatbot de consulta de encuestas")

# Cargar la clave desde un archivo subido
uploaded_file = st.file_uploader("📎 Sube tu archivo JSON de credenciales", type="json")

if uploaded_file:
    # Cargar credenciales
    credentials = service_account.Credentials.from_service_account_info(
        uploaded_file.read(),
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    service = build('sheets', 'v4', credentials=credentials)
    sheet_id = '1wuARCPY8efS3cvJgITE_fCmMNnQx0xHb0ZfWutVDIfo'
    range_name = 'PEDAGOGIA A PIE DE CALLE'

    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_name
    ).execute()

    values = result.get('values', [])

    if not values:
        st.warning("⚠️ No se encontraron datos.")
    else:
        headers = values[0]
        data = values[1:]
        df = pd.DataFrame(data, columns=headers)

        st.success(f"Datos cargados correctamente. Total de encuestas: {len(df)}")

        st.subheader("🔍 Consulta personalizada")

        columna = st.selectbox("Selecciona una columna", df.columns)
        valores = sorted(df[columna].unique())

        valor = st.selectbox("Selecciona un valor", valores)

        coincidencias = df[df[columna] == valor]

        st.info(f"🔎 Se encontraron **{len(coincidencias)}** registros con el valor seleccionado.")

        with st.expander("📋 Ver resultados"):
            st.dataframe(coincidencias)
else:
    st.info("👆 Sube tu archivo JSON de credenciales para comenzar.")
                                                                                                                                                                                                                                                                                            
