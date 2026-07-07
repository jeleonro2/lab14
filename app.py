import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ==========================================================
# GENERACIÓN DE DATOS DIRECTA (Evita errores de lectura CSV)
# ==========================================================
@st.cache_data
def generate_clean_data():
    # Tu semilla asignada (050 -> 50) y cantidad de registros (3050)
    np.random.seed(50)
    num_registros = 3050

    # Variables base
    promedio = np.random.uniform(0, 20, num_registros)
    asistencia = np.random.uniform(40, 100, num_registros)
    ingreso = np.random.normal(2500, 800, num_registros).clip(1025, 8000)
    horas = np.random.poisson(15, num_registros).clip(0, 40)
    edad = np.random.randint(16, 35, num_registros)

    df_internal = pd.DataFrame({
        'promedio_ponderado': promedio,
        'asistencia_porcentaje': asistencia,
        'ingreso_familiar': ingreso,
        'horas_estudio_semanal': horas,
        'edad': edad
    })

    # Variables derivadas obligatorias
    df_internal['riesgo_academico'] = ((df_internal['promedio_ponderado'] < 11.5) & (df_internal['asistencia_porcentaje'] < 70)).astype(int)
    df_internal['horas_por_credito'] = round(df_internal['horas_estudio_semanal'] / df_internal['edad'], 3)
    df_internal['indice_vulnerabilidad'] = round(((20 - df_internal['promedio_ponderado']) * (100 - df_internal['asistencia_porcentaje'])) / (df_internal['ingreso_familiar'] / 100), 3)

    # Variable objetivo lógica (Deserción Universitaria)
    score_desercion = (
        (df_internal['promedio_ponderado'] < 11.5) * 0.4 + 
        (df_internal['asistencia_porcentaje'] < 75) * 0.3 + 
        (df_internal['ingreso_familiar'] < 1500) * 0.2 +
        (df_internal['riesgo_academico'] == 1) * 0.1
    )
    df_internal['desertor'] = (score_desercion > 0.35).astype(int)
    return df_internal

# Carga de datos limpia y segura
df = generate_clean_data()

# ==========================================================
# INTERFAZ DEL DASHBOARD (STREAMLIT)
# ==========================================================
st.title("📊 Dashboard de Control de Deserción Universitaria (Cód: 050)")
st.markdown("Herramienta interactiva para la identificación temprana de alertas académicas.")

# VISUALIZACIÓN 1: Indicador KPI
tasa_desercion = df['desertor'].mean() * 100
st.metric(label="📉 Tasa Global de Deserción", value=f"{tasa_desercion:.2f}%")

col1, col2 = st.columns(2)

with col1:
    # VISUALIZACIÓN 2: Gráfico comparativo (Barras)
    st.subheader("Rendimiento Promedio por Estado")
    fig1, ax1 = plt.subplots()
    sns.barplot(data=df, x='desertor', y='promedio_ponderado', ax=ax1, palette='Set2')
    ax1.set_xticklabels(['Activo', 'Desertor'])
    st.pyplot(fig1)

with col2:
    # VISUALIZACIÓN 3: Distribución estadística (Boxplot)
    st.subheader("Distribución de la Asistencia")
    fig2, ax2 = plt.subplots()
    sns.boxplot(data=df, x='desertor', y='asistencia_porcentaje', ax=ax2, palette='Pastel1')
    ax2.set_xticklabels(['Activo', 'Desertor'])
    st.pyplot(fig2)

# VISUALIZACIÓN 4: Visualización libre (Heatmap de Correlaciones)
st.subheader("🗺️ Mapa de Calor de Factores de Riesgo")
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
st.pyplot(fig3)

# STORYTELLING DE DATOS
st.write("---")
st.header("📖 Storytelling de Datos y Decisiones Estratégicas")
st.subheader("🎯 Hallazgos Principales")
st.write("1. **La asistencia es crítica:** Los alumnos con asistencia inferior al 75% concentran la mayor probabilidad de deserción.")
st.write("2. **Correlación Directa:** El rendimiento académico tiene la correlación negativa más fuerte con el abandono escolar.")
st.write("3. **Barrera Financiera:** Estudiantes con ingresos familiares en el quintil más bajo muestran picos severos en el índice de vulnerabilidad.")

st.subheader("🚀 Recomendaciones Organizacionales")
st.write("- **Plan de Alerta Temprana:** Automatizar alertas cuando un alumno falte a 3 clases consecutivas.")
st.write("- **Tutorías Focalizadas:** Asignar mentores obligatorios a alumnos con `riesgo_academico == 1` antes de los exámenes parciales.")
st.write("- **Becas de Emergencia:** Crear un fondo de contingencia para alumnos con alto índice de vulnerabilidad financiera.")
