# 📊 Proyecto EDA Marketing Bancario — Máster Data & Analytics

Este proyecto forma parte del módulo de *Análisis Exploratorio de Datos (EDA) + Python* del Máster en Data & Analytics.  
El objetivo es realizar un análisis exploratorio y descriptivo de una base de datos bancaria, desarrollando KPIs clave y visualizándolos en un dashboard interactivo.

---

## 🗂 Estructura del Proyecto

El trabajo se ha desarrollado en **5 fases**:

### **Fase 1 — Preparación inicial**
- **Carga de archivos originales**:  
  - `bank-additional.csv`  
  - `customer-details.xlsx`
- Revisión de duplicidades.
- Comprobación y ajuste de tipos de datos.
- Transformaciones globales necesarias para el análisis.
- Transformaciones iniciales columna por columna.
- Detección de columnas vacías o con nulos.
- Preparación del flujo de trabajo para la limpieza final.

### **Fase 2 — Limpieza y transformación de datos**
🎯 **Objetivo**: Consolidar y dejar un único archivo Excel limpio (`data_set_complete.xlsx`) listo para análisis.

Acciones realizadas:
- Eliminación de duplicados.
- Verificación y tratamiento de valores nulos.
- Homogeneización de valores categóricos.
- Conversión de formatos (fechas, enteros, etc.).
- Creación de columnas auxiliares.
- Exportación final de datos limpios y creación de script `.py` para carga de datos.

### **Fase 3 — Análisis Exploratorio (EDA) y cálculo de KPIs**
🎯 **Objetivo**: Calcular los 3 KPIs definidos usando únicamente el dataset limpio.

- **KPI 1**: Promedio de contactos necesarios para lograr una suscripción y desglose por perfiles financieros.
- **KPI 2**: Arquetipo de cliente suscriptor (perfil demográfico, financiero y de contacto).
- **KPI 3**: Relación entre antigüedad como cliente y tasa de suscripción.

Cada KPI se documentó con:
- Lógica de cálculo.
- Tablas de resultados.
- Gráficos de apoyo.

### **Fase 4 — Visualización en Dashboard**
🎯 **Objetivo**: Desarrollar un dashboard interactivo con **Streamlit** para visualizar los KPIs.

Características:
- Tres pestañas (una por KPI).
- Métricas destacadas, tablas y gráficos.
- Anotaciones en gráficos para facilitar la interpretación.
- Diseño adaptable y navegación sencilla.

### **Fase 5 — Informe y documentación**
🎯 **Objetivo**: Documentar todo el proceso y facilitar la reproducibilidad del proyecto.

Este README cumple con:
- Descripción detallada de fases y procesos.
- Explicación de KPIs.
- Instrucciones de instalación y ejecución del dashboard.

---

## 📌 KPIs Implementados

1. **KPI 1** — Promedio de contactos para suscriptores:  
   - Media de llamadas necesarias para una suscripción: **2.06**.
   - Distribución en buckets (1, 2, 3+) con desglose de % con préstamo personal, hipoteca o sin productos previos.

2. **KPI 2** — Arquetipo de cliente suscriptor:  
   - Variables numéricas: edad, ingresos, duración de llamada, número de contactos.
   - Top categorías en ocupación, estado civil, nivel educativo, canal de contacto y productos financieros previos.

3. **KPI 3** — Antigüedad como cliente vs tasa de suscripción:  
   - Clasificación en rangos de antigüedad: `<1 año`, `1-3 años`, `3-5 años`, `5-10 años`, `10+ años`.
   - Cálculo de tasa de conversión por rango.

---

## 🚀 Instrucciones para ejecutar el Dashboard

### 1️⃣ Requisitos previos
- **Python 3.10 o superior**
- **pip** instalado
- Conexión a internet para instalar dependencias
- Archivo limpio: `data_set_complete.xlsx` (39.578 registros, sin duplicados y 0% nulos)

### 2️⃣ Clonar el repositorio
```bash
git clone https://github.com/usuario/proyecto_eda_marketing_bancario.git
cd proyecto_eda_marketing_bancario
```

### 3️⃣ Crear y activar un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
```

**Activarlo:**
- **Mac / Linux**
```bash
source venv/bin/activate
```
- **Windows (PowerShell)**
```powershell
venv\Scripts\activate
```

Si ves `(venv)` al inicio de la línea de comandos, significa que está activo.

### 4️⃣ Instalar dependencias
- **Si tienes el archivo `requirements.txt`:**
```bash
pip install -r requirements.txt
```
- **Si no existe `requirements.txt`:**
```bash
pip install streamlit pandas numpy matplotlib openpyxl
```

### 5️⃣ Colocar el archivo de datos
El dashboard utiliza `data_set_complete.xlsx`, que debe estar en la carpeta raíz del proyecto (junto a `dashboard.py`).

### 6️⃣ Ejecutar el dashboard
```bash
streamlit run dashboard.py
```
Si no se abre automáticamente, copia y pega la URL mostrada en la terminal, por ejemplo:
```
http://localhost:8501
```

### 7️⃣ Navegación en el dashboard
- **KPI 1 — Contactos**
- **KPI 2 — Arquetipo**
- **KPI 3 — Antigüedad**


---

## 📄 Licencia
Este proyecto se comparte bajo licencia MIT. Puedes usarlo, modificarlo y distribuirlo citando la fuente original.
