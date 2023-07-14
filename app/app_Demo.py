import streamlit as st
import pandas as pd
import json
import altair as alt

json_file_path = "instituciones_0007.json"

st.set_page_config(layout="wide")

st.title("Visualizador de Características")

with open(json_file_path, "r") as f:
    data = json.load(f)

df = pd.DataFrame.from_dict(data)

st.write("Datos del archivo JSON:")

# Obtener la lista de instituciones
instituciones = df["Nombre_Institucion"].unique()

# Mostrar las opciones como una lista
selected_institucion = st.sidebar.selectbox("Selecciona una institución:", instituciones)

# Filtrar el DataFrame por la institución seleccionada
df_selected = df[df["Nombre_Institucion"] == selected_institucion]

# Mostrar información de la institución en una lista
st.sidebar.subheader("Información de la institución:")
st.sidebar.text(f"AMIE:\n{df_selected['AMIE'].iloc[0]}")
st.sidebar.text(f"Nombre_Institucion:\n{df_selected['Nombre_Institucion'].iloc[0]}")
st.sidebar.text(f"Provincia:\n{df_selected['Provincia'].iloc[0]}")
st.sidebar.text(f"Codigo_Provincia:\n{df_selected['Codigo_Provincia'].iloc[0]}")
st.sidebar.text(f"Codigo_Canton:\n{df_selected['Codigo_Canton'].iloc[0]}")
st.sidebar.text(f"Canton:\n{df_selected['Canton'].iloc[0]}")
st.sidebar.text(f"Codigo_Parroquia:\n{df_selected['Codigo_Parroquia'].iloc[0]}")
st.sidebar.text(f"Parroquia:\n{df_selected['Parroquia'].iloc[0]}")
st.sidebar.text(f"Zona_Administrativa:\n{df_selected['Zona_Administrativa'].iloc[0]}")

# Crear gráficas por categoría usando el DataFrame filtrado
df_cantones = df[df["Nombre_Institucion"] != selected_institucion].groupby("Canton").size().reset_index(name="num_instituciones")

chart_type_cantones = st.selectbox("Selecciona el tipo de gráfico para cantones:", ["Barras", "Pastel"])

if chart_type_cantones == "Barras":
    chart_cantones = alt.Chart(df_cantones).mark_bar().encode(
        x='Canton',
        y='num_instituciones',
        tooltip='num_instituciones'
    ).interactive()
elif chart_type_cantones == "Pastel":
    chart_cantones = alt.Chart(df_cantones).mark_arc().encode(
        theta='num_instituciones',
        color='Canton',
        tooltip='num_instituciones'
    ).interactive()

st.write("Gráfico de barras o pastel por cantón:")
st.altair_chart(chart_cantones, use_container_width=True)

df_provincias = df[df["Nombre_Institucion"] != selected_institucion].groupby("Provincia").size().reset_index(name="num_instituciones")

chart_type_provincias = st.selectbox("Selecciona el tipo de gráfico para provincias:", ["Barras", "Pastel"])

if chart_type_provincias == "Barras":
    chart_provincias = alt.Chart(df_provincias).mark_bar().encode(
        x='Provincia',
        y='num_instituciones',
        tooltip='num_instituciones'
    ).interactive()
elif chart_type_provincias == "Pastel":
    chart_provincias = alt.Chart(df_provincias).mark_arc().encode(
        theta='num_instituciones',
        color='Provincia',
        tooltip='num_instituciones'
    ).interactive()

st.write("Gráfico de barras o pastel por provincia:")
st.altair_chart(chart_provincias, use_container_width=True)

df_parroquias = df[df["Nombre_Institucion"] != selected_institucion].groupby("Parroquia").size().reset_index(name="num_instituciones")

chart_type_parroquias = st.selectbox("Selecciona el tipo de gráfico para parroquias:", ["Barras", "Pastel"])

if chart_type_parroquias == "Barras":
    chart_parroquias = alt.Chart(df_parroquias).mark_bar().encode(
        x='Parroquia',
        y='num_instituciones',
        tooltip='num_instituciones'
    ).interactive()
elif chart_type_parroquias == "Pastel":
    chart_parroquias = alt.Chart(df_parroquias).mark_arc().encode(
        theta='num_instituciones',
        color='Parroquia',
        tooltip='num_instituciones'
    ).interactive()

st.write("Gráfico de barras o pastel por parroquia:")
st.altair_chart(chart_parroquias, use_container_width=True)
