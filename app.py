import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="YACIMIENTO AI",
    page_icon="🛢️",
    layout="wide"
)



st.title("🛢️ YACIMIENTO AI")
st.subheader("Sistema inteligente para el análisis y monitoreo de pozos")

st.write(
    "Analiza el historial de los pozos, detecta anomalías, "
    "clasifica niveles de riesgo y prioriza intervenciones."
)

st.divider()

st.markdown("### 🔎 ¿Cómo funciona YACIMIENTO AI?")
st.caption("Del dato histórico a una decisión operativa.")


col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("**1️⃣ Analizar**")
        st.write("Procesa el historial y las variables de cada pozo.")

with col2:
    with st.container(border=True):
        st.markdown("**2️⃣ Detectar**")
        st.write("Identifica anomalías y clasifica el nivel de riesgo.")

with col3:
    with st.container(border=True):
        st.markdown("**3️⃣ Priorizar**")
        st.write("Establece prioridades para facilitar la intervención.")




st.divider()

st.header("📂 Cargar historial de pozos")
st.caption("Cargá los datos históricos para comenzar el análisis.")

archivo = st.file_uploader(
    "Seleccioná el archivo histórico de los pozos",
    type=["csv", "xlsx", "xls"]
)
if archivo is not None:

    if archivo.name.lower().endswith(".csv"):
        df_app = pd.read_csv(archivo)
    else:
        df_app = pd.read_excel(archivo)

    # Limpiar espacios invisibles en los nombres de columnas
    df_app.columns = (
        df_app.columns
        .astype(str)
        .str.strip()
    )

    st.success("✅ Archivo cargado correctamente")
    st.write(df_app.columns)

    st.write(f"**Cantidad de registros:** {len(df_app)}")
    st.write(f"**Cantidad de columnas:** {len(df_app.columns)}")

    st.subheader("📋 Datos cargados")
    st.write("Nombres de las columnas:", df_app.columns.tolist())



    st.dataframe(
        df_app,
        use_container_width=True
    )

    st.divider()

    # =========================
    # INDICADORES
    # =========================

    st.header("📊 Indicadores")

    col1, col2, col3 = st.columns(3)

    with col1:

        if "Pozo" in df_app.columns:
            total_pozos = df_app["Pozo"].nunique()
        else:
            total_pozos = 0

        st.metric(
            "🛢️ Pozos analizados",
            total_pozos
        )

    with col2:

        if "Anomalias" in df_app.columns:

            total_anomalias = pd.to_numeric(
                df_app["Anomalias"],
                errors="coerce"
            ).fillna(0).sum()

        elif "Porcentaje_anomalias" in df_app.columns:

            total_anomalias = (
                pd.to_numeric(
                    df_app["Porcentaje_anomalias"],
                    errors="coerce"
                ).fillna(0) > 0
            ).sum()

        else:
            total_anomalias = 0

        st.metric(
            "⚠️ Anomalías detectadas",
            int(total_anomalias)
        )

    with col3:

        columna_riesgo = None

        if "Nivel de Riesgo" in df_app.columns:
            columna_riesgo = "Nivel de Riesgo"

        elif "Nivel_Riesgo" in df_app.columns:
            columna_riesgo = "Nivel_Riesgo"

        if columna_riesgo:

            alto = (
                df_app[columna_riesgo]
                .astype(str)
                .str.upper()
                .eq("ALTO")
                .sum()
            )

        else:
            alto = 0

        st.metric(
            "🔴 Pozos de alto riesgo",
        
            alto
        )

    # =========================
    # NIVEL DE RIESGO
    # =========================

    st.divider()

    st.header("⚠️ Evaluación del nivel de riesgo")
    st.caption("Clasificación de los pozos según el nivel de riesgo identificado.")

    if columna_riesgo:

        riesgo = df_app[columna_riesgo].value_counts()

        st.bar_chart(riesgo)
        st.subheader("🚨 Pozos que requieren atención prioritaria")
        st.caption("detalle de los pozos clasificados con mayor nivel de riesgo.")



   

        tabla_alto = df_app[
            df_app[columna_riesgo]
            .astype(str)
            .str.upper()
            == "ALTO"
        ]

        st.dataframe(
            tabla_alto,
            use_container_width=True
        )

    else:

        st.warning(
            "No se encontró una columna de nivel de riesgo."
        )

# =========================
    # PRIORIDAD DE INTERVENCIÓN
    # =========================

    st.divider()
    st.header("🎯 Priorización de intervenciones")
    st.caption("Orden de intervención según el nivel de prioridad detectado.")

   

    columna_prioridad = None

    for columna in df_app.columns:
        valores = (
            df_app[columna]
            .astype(str)
            .str.upper()
            .str.strip()
        )

        if valores.isin(["ALTA", "MEDIA", "BAJA"]).sum() > 0:
            columna_prioridad = columna
            break

    if columna_prioridad is not None:

        st.write(
            f"Columna detectada: **{columna_prioridad}**"
        )
        st.subheader("📊 Resumen del análisis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🔴 Prioridad ALTA",
                (
                    df_app[columna_prioridad]
                    .astype(str)
                    .str.upper()
                    .eq("ALTA")
                    .sum()
                )
            )

        with col2:
            st.metric(
                "🟠 Prioridad MEDIA",
                (
                    df_app[columna_prioridad]
                    .astype(str)
                    .str.upper()
                    .eq("MEDIA")
                    .sum()
                )
            )

        with col3:
            st.metric(
                "🟢 Prioridad BAJA",
                (
                    df_app[columna_prioridad]
                    .astype(str)
                    .str.upper()
                    .eq("BAJA")
                    .sum()
                )
            )

        st.subheader("📋 Pozos según prioridad")
        st.subheader("🛠️ Recomendaciones para la toma de decisiones")
        st.caption("Acciones sugeridas según la prioridad detectada por el sistema.")
        

        if columna_prioridad is not None:

            tabla_recomendaciones = df_app.copy()

            tabla_recomendaciones["Recomendación de acción"] = (
                tabla_recomendaciones[columna_prioridad]
                .astype(str)
                .str.upper()
                .map({
                    "ALTA": "Inspección prioritaria",
                    "MEDIA": "Monitoreo reforzado",
                    "BAJA": "Monitoreo normal"
                })
            )

            st.dataframe(
                tabla_recomendaciones[
                    ["Pozo", columna_prioridad, "Recomendación de acción"]
                ],
                use_container_width=True
            )

        st.dataframe(
            df_app,
            use_container_width=True
        )

    else:

        st.warning(
            "No se encontró una columna con prioridades ALTA, MEDIA o BAJA."
        )
        st.divider()

st.header("📌 Resumen ejecutivo")
st.caption("Síntesis de los principales resultados obtenidos a partir del historial analizado.")

st.write(
    "YACIMIENTO AI analiza el historial de los pozos, "
    "detecta anomalías, clasifica el nivel de riesgo "
    "y establece prioridades de intervención para "
    "facilitar la toma de decisiones."
)
st.divider()

st.header("📥 Descargar análisis")
st.caption("Descargá los resultados del análisis para continuar trabajando con la información.")

if "df_app" in locals():

    csv_descarga = df_app.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Descargar resultados en CSV",
        data=csv_descarga,
        file_name="YACIMIENTO_AI_resultados.csv",
        mime="text/csv"
    )