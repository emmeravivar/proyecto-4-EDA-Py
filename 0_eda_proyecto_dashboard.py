import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="EDA Marketing Bancario — Dashboard", layout="wide")

# -----------------------------
# Utilidades
# -----------------------------
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    # Normalizar columnas clave
    if 'Dt_Customer' in df.columns:
        df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], errors='coerce')
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Normalizar 'y' a booleano
    if 'y' in df.columns:
        if df['y'].dtype == bool:
            pass
        elif df['y'].dtype == object:
            mapa = {True: True, False: False, 'yes': True, 'no': False, 'Yes': True, 'No': False, 1: True, 0: False}
            df['y'] = df['y'].map(mapa)
            df['y'] = df['y'].fillna(False).astype(bool)
        else:
            df['y'] = df['y'].astype(bool)

    # Tipos numéricos esperados si existen
    for col in ['campaign', 'loan', 'housing']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def kpi1_calculos(df: pd.DataFrame):
    """ KPI 1: promedio de contactos para suscriptores y desglose 1 / 2 / 3+ """
    sus = df[df['y'] == True].copy()

    media_contactos = float(sus['campaign'].mean()) if 'campaign' in sus.columns else np.nan

    def bucketize(n):
        if pd.isna(n):
            return np.nan
        n = int(n)
        if n <= 1: return '1'
        if n == 2: return '2'
        return '3+'

    if 'campaign' in sus.columns:
        sus['bucket'] = sus['campaign'].apply(bucketize)

    resultados = None
    if set(['loan', 'housing', 'bucket']).issubset(sus.columns):
        agg = []
        for b in ['1', '2', '3+']:
            tmp = sus[sus['bucket'] == b]
            if len(tmp) == 0:
                agg.append((b, 0, 0.0, 0.0, 0.0))
                continue
            p_loan = (tmp['loan'] == 1).mean() * 100
            p_housing = (tmp['housing'] == 1).mean() * 100
            p_sin = ((tmp['loan'] == 0) & (tmp['housing'] == 0)).mean() * 100
            agg.append((b, len(tmp), p_loan, p_housing, p_sin))
        resultados = pd.DataFrame(agg, columns=['bucket', 'suscriptores', '%_loan', '%_housing', '%_sin_prev'])

    return media_contactos, resultados


def kpi2_arquetipo(df: pd.DataFrame):
    """ KPI 2: arquetipo del cliente suscriptor """
    sus = df[df['y'] == True].copy()

    resumen = {}
    for col in ['age', 'Income', 'duration', 'campaign']:
        if col in sus.columns:
            resumen[col] = {
                'count': int(sus[col].notna().sum()),
                'mean': float(sus[col].mean()),
                'median': float(sus[col].median()),
                'min': float(sus[col].min()),
                'max': float(sus[col].max()),
            }

    topcats = {}
    for col in ['job', 'marital', 'education', 'contact', 'housing', 'loan']:
        if col in sus.columns:
            vc = sus[col].value_counts(dropna=True)
            topcats[col] = vc.head(5)

    return resumen, topcats


def kpi3_antiguedad(df: pd.DataFrame):
    """ KPI 3: antigüedad del cliente vs % suscripción """
    if 'Dt_Customer' in df.columns and 'date' in df.columns:
        years = (df['date'] - df['Dt_Customer']).dt.days / 365.25
        df = df.assign(customer_years=years)

        bins = [0, 1, 3, 5, 10, np.inf]
        labels = ['<1 año', '1-3 años', '3-5 años', '5-10 años', '10+ años']
        df['antigüedad_rango'] = pd.cut(
            df['customer_years'], bins=bins, labels=labels, right=False
        ).astype('category')
        df['antigüedad_rango'] = df['antigüedad_rango'].cat.set_categories(labels, ordered=True)

        tabla = (
            df.groupby('antigüedad_rango', observed=True)
              .agg(total_clientes=('y', 'count'),
                   total_suscritos=('y', lambda s: (s == True).sum()))
              .reset_index()
        )
        tabla['porcentaje_suscripcion'] = tabla['total_suscritos'] / tabla['total_clientes'] * 100
        return df, tabla

    return df.assign(customer_years=np.nan, antigüedad_rango=np.nan), pd.DataFrame()


# -----------------------------
# Sidebar / Entrada de datos
# -----------------------------
st.sidebar.header("Datos")
default_path = "data_set_complete.xlsx"
file = st.sidebar.file_uploader("Sube el Excel limpio (data_set_complete.xlsx)", type=["xlsx"])

if file is not None:
    df = load_data(file)
else:
    if os.path.exists(default_path):
        df = load_data(default_path)
    else:
        st.error("No se encontró el archivo 'data_set_complete.xlsx'. Súbelo desde la barra lateral.")
        st.stop()

st.sidebar.success(f"Registros cargados: {len(df):,}")

# -----------------------------
# Cabecera
# -----------------------------
st.title("Dashboard — EDA Marketing Bancario")
st.caption("KPIs: (1) Contactos por suscripción, (2) Arquetipo de cliente, (3) Antigüedad vs conversión")

tab1, tab2, tab3 = st.tabs(["KPI 1 — Contactos", "KPI 2 — Arquetipo", "KPI 3 — Antigüedad"])

# -----------------------------
# KPI 1
# -----------------------------
with tab1:
    st.subheader("Promedio de contactos necesarios para lograr una suscripción")
    media_contactos, tabla_kpi1 = kpi1_calculos(df)

    cols = st.columns(3)
    cols[0].metric("Promedio de contactos", f"{media_contactos:.2f}" if media_contactos == media_contactos else "—")
    cols[0].caption("Media de llamadas para suscriptores")

    if 'campaign' in df.columns:
        cols[1].write(f"Total suscriptores considerados: {int((df['y'] == True).sum()):,}")
        cols[2].write("Buckets: 1, 2, 3+ llamadas")

    if tabla_kpi1 is not None:
        # Formato tabla
        st.dataframe(
            tabla_kpi1.style.format({
                'suscriptores': '{:,}',
                '%_loan': '{:.1f}%',
                '%_housing': '{:.1f}%',
                '%_sin_prev': '{:.1f}%'
            }),
            use_container_width=True
        )

        # Gráfico barras agrupadas
        fig = plt.figure()
        x = np.arange(len(tabla_kpi1['bucket']))
        width = 0.25
        bars_loan = plt.bar(x - width, tabla_kpi1['%_loan'], width, label='% loan')
        bars_housing = plt.bar(x, tabla_kpi1['%_housing'], width, label='% housing')
        bars_sin = plt.bar(x + width, tabla_kpi1['%_sin_prev'], width, label='% sin prev')
        plt.xticks(x, tabla_kpi1['bucket'])
        plt.xlabel("Número de llamadas")
        plt.ylabel("Porcentaje (%)")
        plt.title("Perfil financiero de suscriptores por número de llamadas")
        plt.legend()

        # Anotar %
        for bars in [bars_loan, bars_housing, bars_sin]:
            for b in bars:
                h = b.get_height()
                plt.annotate(f"{h:.1f}%",
                             xy=(b.get_x() + b.get_width()/2, h),
                             xytext=(0, 3), textcoords="offset points",
                             ha='center', va='bottom', fontsize=8)

        st.pyplot(fig)

# -----------------------------
# KPI 2
# -----------------------------
with tab2:
    st.subheader("Arquetipo de cliente que contrata productos bancarios")
    resumen, topcats = kpi2_arquetipo(df)

    # Resumen numérico
    if resumen:
        tbl = pd.DataFrame(resumen).T
        st.write("**Variables numéricas (suscriptores):**")
        st.dataframe(
            tbl.style.format({
                'count': '{:,}',
                'mean': '{:.2f}',
                'median': '{:.2f}',
                'min': '{:.2f}',
                'max': '{:.2f}',
            }),
            use_container_width=True
        )
    else:
        st.info("No se encontraron variables numéricas esperadas para el arquetipo.")

    # Top categorías
    if topcats:
        st.write("**Top categorías (suscriptores):**")
        for col, serie in topcats.items():
            st.write(f"**{col}**")
            st.dataframe(serie.to_frame(name='frecuencia').style.format({'frecuencia': '{:,}'}), use_container_width=True)

        # Gráfico simple: top-5 job si existe
        if 'job' in topcats and len(topcats['job']) > 0:
            fig2 = plt.figure()
            topcats['job'].sort_values(ascending=True).plot(kind='barh')
            plt.title("Top-5 ocupaciones entre suscriptores")
            plt.xlabel("Frecuencia")
            plt.tight_layout()
            st.pyplot(fig2)
    else:
        st.info("No se encontraron columnas categóricas esperadas para el arquetipo.")

# -----------------------------
# KPI 3
# -----------------------------
with tab3:
    st.subheader("Relación entre antigüedad como cliente y tasa de suscripción")
    df_kpi3, tabla_kpi3 = kpi3_antiguedad(df)

    if not tabla_kpi3.empty:
        st.dataframe(
            tabla_kpi3.style.format({
                'total_clientes': '{:,}',
                'total_suscritos': '{:,}',
                'porcentaje_suscripcion': '{:.2f}%'
            }),
            use_container_width=True
        )

        # Orden fijo para el gráfico
        orden = ['<1 año', '1-3 años', '3-5 años', '5-10 años', '10+ años']
        tabla_plot = tabla_kpi3.copy()
        tabla_plot['antigüedad_rango'] = pd.Categorical(tabla_plot['antigüedad_rango'], categories=orden, ordered=True)
        tabla_plot = tabla_plot.sort_values('antigüedad_rango')

        fig3 = plt.figure()
        bars = plt.bar(tabla_plot['antigüedad_rango'].astype(str), tabla_plot['porcentaje_suscripcion'])
        plt.xlabel("Antigüedad")
        plt.ylabel("% suscripción")
        plt.title("Tasa de suscripción por antigüedad (%)")
        plt.tight_layout()

        # Anotar %
        for b in bars:
            h = b.get_height()
            plt.annotate(f"{h:.2f}%",
                         xy=(b.get_x() + b.get_width()/2, h),
                         xytext=(0, 3), textcoords="offset points",
                         ha='center', va='bottom', fontsize=8)

        st.pyplot(fig3)

        min_years = float(np.nanmin(df_kpi3['customer_years'].values))
        max_years = float(np.nanmax(df_kpi3['customer_years'].values))
        st.caption(f"Antigüedad mínima: {min_years:.2f} años | máxima: {max_years:.2f} años · Base: {len(df):,} registros")
    else:
        st.info("No hay datos suficientes para calcular la antigüedad. Asegúrate de tener 'Dt_Customer' y 'date'.")