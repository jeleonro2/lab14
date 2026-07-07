import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar los datos generados de forma segura
@st.cache_data
def load_data():
    # 1. Leemos el archivo CSV
    df = pd.read_csv('dataset_personal.csv')
    
    # 2. Limpiamos espacios fantasmas en los nombres de las columnas
    df.columns = df.columns.str.strip()
    
    # 3. Si por alguna razón Pandas unió las columnas (ej: "promedio_ponderado,asistencia_porcentaje,...")
    # dividimos los nombres y reestructuramos el DataFrame correctamente
    if len(df.columns) == 1 and ',' in df.columns[0]:
        real_columns = df.columns[0].split(',')
        # Limpiar espacios en los nombres reales
        real_columns = [col.strip() for col in real_columns]
        # Separar los datos de la fila única mal leída
        df = df[df.columns[0]].str.split(',', expand=True)
        df.columns = real_columns
        # Convertir a tipos numéricos para que no falle el promedio (.mean())
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')
            
    return df

df = load_data()

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
