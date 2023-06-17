import streamlit as st
import pandas as pd
import json
import altair as alt

json_file_path = "instituciones_0007.json"

st.title("Visualizador de Características")

with open(json_file_path, "r") as f:
    data = json.load(f)

df = pd.DataFrame.from_dict(data)

st.write("Datos del archivo JSON:")
st.dataframe(df)

df_cantones = df.groupby("Canton").agg(num_instituciones=("Nombre_Institucion", "count")).reset_index()

chart_cantones = alt.Chart(df_cantones).mark_bar().encode(
    x='Canton',
    y='num_instituciones',
    tooltip='num_instituciones'
).interactive()

st.write("Gráfica de barras por cantón:")
st.altair_chart(chart_cantones, use_container_width=True)

df_provincias = df.groupby("Provincia").agg(num_instituciones=("Nombre_Institucion", "count")).reset_index()

chart_provincias = alt.Chart(df_provincias).mark_bar().encode(
    x='Provincia',
    y='num_instituciones',
    tooltip='num_instituciones'
).interactive()

st.write("Gráfica de barras por provincia:")
st.altair_chart(chart_provincias, use_container_width=True)

df_parroquias = df.groupby("Parroquia").agg(num_instituciones=("Nombre_Institucion", "count")).reset_index()

chart_parroquias = alt.Chart(df_parroquias).mark_bar().encode(
    x='Parroquia',
    y='num_instituciones',
    tooltip='num_instituciones'
).interactive()

st.write("Gráfica de barras por parroquia:")
st.altair_chart(chart_parroquias, use_container_width=True)
