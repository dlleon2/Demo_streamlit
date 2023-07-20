import streamlit as st
import pandas as pd
import sqlite3
import json
import altair as alt

# Nombre del archivo JSON
json_file_path = "instituciones_0007.json"

# Nombre de la base de datos SQLite
db_name = "base_de_datos_app.db"

# Crear la base de datos y la tabla si no existen
def crear_base_de_datos():
    db_conn = sqlite3.connect(db_name)
    cursor = db_conn.cursor()

    tabla_sql = """
    CREATE TABLE IF NOT EXISTS instituciones (
        AMIE TEXT PRIMARY KEY,
        Nombre_Institucion TEXT,
        Provincia TEXT,
        Codigo_Provincia TEXT,
        Codigo_Canton TEXT,
        Canton TEXT,
        Codigo_Parroquia TEXT,
        Parroquia TEXT,
        Zona_Administrativa TEXT
    )
    """
    cursor.execute(tabla_sql)

    db_conn.commit()
    db_conn.close()

# Función para cargar los datos del archivo JSON a la base de datos SQLite
def cargar_datos_a_base_de_datos():
    with open(json_file_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame.from_dict(data)

    db_conn = sqlite3.connect(db_name)
    df.to_sql("instituciones", db_conn, if_exists="replace", index=False)
    db_conn.close()

# Crear la base de datos y cargar los datos si aún no existen
crear_base_de_datos()
cargar_datos_a_base_de_datos()

# Obtener la conexión a la base de datos SQLite
db_conn = sqlite3.connect(db_name)

st.set_page_config(layout="wide")

st.title("Visualizador de Características")

# Realizar la consulta a la base de datos y obtener los datos como DataFrame
query = "SELECT * FROM instituciones"
df = pd.read_sql(query, db_conn)

st.write("Datos de la base de datos SQLite:")

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

# Cierra la conexión a la base de datos al finalizar
db_conn.close()
