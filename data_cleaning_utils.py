# data_cleaning_utils.py

import pandas as pd
from datetime import datetime

def convertir_a_entero(df, columnas):
    df = df.copy()
    for col in columnas:
        print(f"🔍 Procesando columna '{col}'...")

        # Convertir a numérico, forzando coerción en caso de error
        df[col] = pd.to_numeric(df[col], errors='coerce')

        # Convertir a tipo entero que permite nulos
        df[col] = df[col].astype('Int64')

        # Mostrar valores únicos y control de nulos
        print("✅ Columna convertida a Int64.")
        print("🔎 Valores únicos después:", df[col].unique())
        print(f"⚠️ Nulos detectados: {df[col].isnull().sum()}")
        print("-" * 50)
    return df

def convertir_a_booleano(df, columna, mapa):
    df = df.copy()

    # Paso 1: Normalizar texto
    df[columna] = df[columna].astype(str).str.lower().str.strip()

    # Paso 2: Identificar valores no válidos
    valores_unicos = set(df[columna].unique())
    valores_mapeables = set(mapa.keys())
    valores_no_validos = valores_unicos - valores_mapeables

    if valores_no_validos:
        print(f"⚠️ Valores no válidos encontrados en '{columna}': {valores_no_validos}")

    # Paso 3: Aplicar mapeo
    df[columna] = df[columna].map(mapa)

    # Paso 4: Reportar valores nulos después del mapeo
    nulos = df[columna].isnull().sum()
    print(f"✅ Columna '{columna}' convertida a booleano.")
    print(f"🔍 Nulos después del mapeo: {nulos}")
    print(f"🔎 Valores únicos finales: {df[columna].unique()}")

    return df

def homogeneizar_categoricas(df, columnas):
    df = df.copy()
    for col in columnas:
        print(f"🔍 Procesando columna '{col}'...")

        # Paso 1: Contar nulos antes
        n_nulos_antes = df[col].isnull().sum()
        print(f"🔎 Nulos antes de transformación: {n_nulos_antes}")

        # Paso 2: Normalizar texto
        df[col] = df[col].astype(str).str.lower().str.strip()

        # Paso 3: Reconvertir 'nan' como string a np.nan
        df[col] = df[col].replace('nan', pd.NA)

        # Paso 4: Convertir a tipo categoría
        df[col] = df[col].astype('category')

        # Paso 5: Mostrar valores únicos y nulos
        print(f"✅ Columna '{col}' homogeneizada y convertida a categórica.")
        print("🔎 Valores únicos:", df[col].unique())
        print(f"⚠️ Nulos después de transformación: {df[col].isnull().sum()}")
        print("-" * 50)
    return df

# Normalización de columnas: imputación mediana
def imputar_mediana(df, columnas):
    for col in columnas:
        mediana = df[col].median()
        df[col] = df[col].fillna(mediana)
        print(f"🧬 Columna '{col}': imputada con mediana = {mediana:.2f}")
    return df

def limpiar_education(df, columna='education'):
    df = df.copy()

    print(f"🔍 Transformando columna '{columna}'...")

    mapeo_education = {
        'basic.4y': 'basic education',
        'basic.6y': 'basic education',
        'basic.9y': 'basic education',
        'high.school': 'high school',
        'professional.course': 'professional training',
        'university.degree': 'university degree',
        'illiterate': 'illiterate'
    }

    df[columna] = df[columna].map(mapeo_education).astype('category')

    print(f"✅ Columna '{columna}' limpiada y convertida a categoría.")
    print(f"🔎 Nuevos valores únicos: {df[columna].unique()}")
    print("-" * 50)
    return df


# funciones para KPI
def resumen_variable_numerica(df, columna):
    print(f"📊 Análisis de la variable numérica: {columna}")
    print("-" * 50)
    print(f"Media: {df[columna].mean():.2f}")
    print(f"Mediana: {df[columna].median():.2f}")
    print(f"Desviación estándar: {df[columna].std():.2f}")
    print(f"Valor mínimo: {df[columna].min()}")
    print(f"Valor máximo: {df[columna].max()}")
    print(f"Percentil 25: {df[columna].quantile(0.25)}")
    print(f"Percentil 50 (mediana): {df[columna].quantile(0.50)}")
    print(f"Percentil 75: {df[columna].quantile(0.75)}")
    print("-" * 50)
    print()


def resumen_variable_categorica(df, columna):
    print(f"\n📊 Análisis de la variable categórica: {columna}")
    print("-" * 50)
    # Conteo absoluto
    conteo = df[columna].value_counts()
    # Porcentaje
    porcentaje = df[columna].value_counts(normalize=True) * 100 
    # Moda
    moda = df[columna].mode()[0]
    # Mostrar resultados
    resumen = pd.DataFrame({
        'Frecuencia': conteo,
        'Porcentaje (%)': porcentaje.round(2)
    })
    
    display(resumen)
    print("🎯 Valor más común (moda): {moda}")
    print("-" * 50)





def convertir_a_fecha(fecha_str):
    meses_es = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

    try:
        if isinstance(fecha_str, str):
            fecha_str = fecha_str.strip().lower()
            partes = fecha_str.split('-')
            if len(partes) == 3:
                dia = partes[0].zfill(2)
                mes = meses_es.get(partes[1])
                anio = partes[2]
                if mes:
                    fecha_formateada = f"{anio}-{mes}-{dia}"
                    return pd.to_datetime(fecha_formateada, format='%Y-%m-%d', errors='coerce')
    except Exception as e:
        print(f"❌ Error con fecha '{fecha_str}': {e}")
    return pd.NaT

def normalizar_ids(df, columnas):
    df = df.copy()
    for col in columnas:
        print(f"🔍 Procesando columna '{col}' (ID)...")

        # Normalizar como texto
        df[col] = df[col].astype(str).str.strip().str.lower()

        # Contar nulos
        n_nulos = df[col].isnull().sum()
        print(f"⚠️ Nulos detectados en '{col}': {n_nulos}")

        # Mostrar muestra de valores únicos (limitado a 5 por claridad)
        valores_unicos = df[col].dropna().unique()
        print(f"🔎 Muestra de valores únicos en '{col}': {valores_unicos[:5]} ...")
        print("-" * 50)

    return df

# Normalización de columnas: education

# Normalización de columnas: poutcome
def limpiar_poutcome(df, columna='poutcome'):
    df = df.copy()

    print(f"🔍 Transformando columna '{columna}'...")

    # Diccionario de mapeo de valores originales a categorías más limpias
    mapeo_poutcome = {
        'nonexistent': 'no previous contact',
        'failure': 'previous contact failed',
        'success': 'previous contact succeeded'
    }

    # Aplicamos el mapeo y convertimos en categoría
    df[columna] = df[columna].map(mapeo_poutcome).astype('category')

    # Confirmación visual del proceso
    print(f"✅ Columna '{columna}' limpiada y convertida a categoría.")
    print(f"🔎 Nuevos valores únicos: {df[columna].unique()}")
    print(f"⚠️ Valores no mapeados (NaN): {df[columna].isna().sum()}")
    print("-" * 50)

    return df

# Normalización de columnas: default
def imputar_default(row):
    if pd.isna(row['default']):
        # Comprobar que no sean NA antes de comparar
        tiene_hipoteca = row['housing'] == 1 if not pd.isna(row['housing']) else False
        tiene_prestamo = row['loan'] == 1 if not pd.isna(row['loan']) else False

        if tiene_hipoteca or tiene_prestamo:
            return 0
        else:
            return pd.NA
    else:
        return row['default']




# Normalización de columnas: imputación moda
def imputar_moda(df, columna):
    """
    Imputa valores nulos de una columna categórica con la moda (valor más frecuente).
    """
    moda = df[columna].mode(dropna=True)[0]
    df[columna] = df[columna].fillna(moda)
    print(f"🎓 Columna '{columna}' imputada con moda = '{moda}'")
    return df









def convertir_a_float(df, columnas):
    df = df.copy()
    for col in columnas:
        print(f"🔍 Procesando columna '{col}' (float)...")

        df[col] = pd.to_numeric(df[col], errors='coerce').astype('float64')

        n_nulos = df[col].isnull().sum()
        n_negativos = (df[col] < 0).sum()
        
        print(f"✅ Columna '{col}' convertida a float64.")
        print(f"⚠️ Nulos detectados: {n_nulos}")
        print(f"⚠️ Valores negativos detectados: {n_negativos}")
        print(f"🔎 Estadísticas de '{col}':")
        print(df[col].describe())
        print("-" * 50)

    return df