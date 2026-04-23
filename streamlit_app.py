import streamlit as st

import pandas as pd

import numpy as np

from datetime import datetime

import os



# Configuración de la página

st.set_page_config(

    page_title="Dashboard - Control de Auditorías",

    page_icon="📊",

    layout="wide",

    initial_sidebar_state="expanded"

)



# Estilos CSS personalizados

st.markdown("""

    <style>

    .metric-card {

        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

        padding: 20px;

        border-radius: 12px;

        color: white;

        text-align: center;

        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

    }

    

    .metric-value {

        font-size: 2.5rem;

        font-weight: bold;

        margin: 10px 0;

    }

    

    .metric-label {

        font-size: 0.9rem;

        opacity: 0.9;

        text-transform: uppercase;

        letter-spacing: 1px;

    }

    

    .color-positive {

        color: #28a745;

        font-weight: bold;

    }

    

    .color-negative {

        color: #dc3545;

        font-weight: bold;

    }

    

    .color-warning {

        color: #fd7e14;

        font-weight: bold;

    }

    

    h1, h2, h3 {

        color: #667eea;

    }

    

    /* Centrar todas las tablas */

    [data-testid="stDataFrame"] {

        margin: 0 auto !important;

        width: 100% !important;

    }

    

    [data-testid="stDataFrame"] > div {

        display: flex !important;

        justify-content: center !important;

    }

    

    /* Centrar contenido de las celdas */

    [data-testid="stDataFrame"] table {

        width: 100% !important;

        margin: 0 auto !important;

    }

    

    [data-testid="stDataFrame"] thead th {

        text-align: center !important;

        font-weight: bold !important;

    }

    

    [data-testid="stDataFrame"] tbody td {

        text-align: center !important;

        padding: 8px !important;

    }

    

    /* Centrar contenedores de tabs */

    .stTabs [role="tablist"] {

        justify-content: center !important;

    }

    

    /* Centrar texto de subheaders */

    h2, h3 {

        text-align: center !important;

    }

    

    /* Contenedor principal centrado */

    .stTab {

        display: flex !important;

        justify-content: center !important;

    }

    

    </style>

""", unsafe_allow_html=True)



# Función auxiliar para encontrar archivos Excel

def encuentra_archivo_excel(filename):

    """Busca un archivo Excel en múltiples ubicaciones posibles"""

    possible_paths = [

        filename,  # Ruta relativa simple

        os.path.join(os.getcwd(), filename),  # Directorio actual

        os.path.join(os.path.dirname(__file__), filename),  # Directorio del script

    ]

    

    # Primero intentar rutas exactas

    for path in possible_paths:

        if os.path.exists(path):

            return path

    

    # Si no encuentra, buscar en el directorio actual con búsqueda insensible a mayúsculas

    current_dir = os.getcwd()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    

    for search_dir in [current_dir, script_dir]:

        try:

            if os.path.isdir(search_dir):

                for file in os.listdir(search_dir):

                    if file.lower() == filename.lower() and file.endswith('.xlsx'):

                        full_path = os.path.join(search_dir, file)

                        return full_path

        except (PermissionError, OSError):

            pass

    

    return None



def descargar_de_github(filename, token=None):

    """Descarga un archivo de GitHub como última opción"""

    try:

        import urllib.request

        

        # URLs del repositorio

        raw_url = f"https://raw.githubusercontent.com/isaac24012000-oss/REPORTE-CALIDAD-FTTH/main/{filename}"

        

        # Crear temporalmente el archivo

        current_dir = os.getcwd()

        filepath = os.path.join(current_dir, filename)

        

        # Descargar

        urllib.request.urlretrieve(raw_url, filepath)

        return filepath

    except Exception as e:

        return None



# Funciones para colorear valores

def colorear_impacto_desviacion(val):

    """Colorea valores de Impacto y Desviación: rojo si negativo, verde si positivo"""

    if pd.isna(val) or val == '-':

        return ''

    try:

        valor_str = str(val).strip().replace('%', '')

        numero = float(valor_str)

        if numero < 0:

            return 'color: #dc3545; font-weight: bold'

        elif numero > 0:

            return 'color: #28a745; font-weight: bold'

    except:

        pass

    return ''



def colorear_intensidad(val):

    """Colorea Intensidad: rojo=Alta, naranja=Media, verde=Bajo"""

    if pd.isna(val) or val == '-':

        return ''

    val_lower = str(val).lower()

    if 'alta' in val_lower:

        return 'color: #dc3545; font-weight: bold'

    elif 'media' in val_lower:

        return 'color: #fd7e14; font-weight: bold'

    elif 'bajo' in val_lower or 'baja' in val_lower:

        return 'color: #28a745; font-weight: bold'

    return ''



def aplicar_colores_df(df):

    """Aplica colores al DataFrame para columnas específicas"""

    df_coloreado = df.copy()

    

    # Colorear Impacto (%)

    if 'Impacto (%)' in df_coloreado.columns:

        def colorear_impacto_val(x):

            try:

                valor_str = str(x).strip().replace('%', '')

                numero = float(valor_str)

                if numero < 0:

                    return f'<span style="color: #dc3545; font-weight: bold">{x}</span>'

                elif numero > 0:

                    return f'<span style="color: #28a745; font-weight: bold">{x}</span>'

            except:

                pass

            return x

        

        df_coloreado['Impacto (%)'] = df_coloreado['Impacto (%)'].apply(colorear_impacto_val)

    

    # Colorear Desviación

    if 'Desviación' in df_coloreado.columns:

        def colorear_desviacion_val(x):

            try:

                valor_str = str(x).strip().replace('%', '')

                numero = float(valor_str)

                if numero < 0:

                    return f'<span style="color: #dc3545; font-weight: bold">{x}</span>'

                elif numero > 0:

                    return f'<span style="color: #28a745; font-weight: bold">{x}</span>'

            except:

                pass

            return x

        

        df_coloreado['Desviación'] = df_coloreado['Desviación'].apply(colorear_desviacion_val)

    

    # Colorear Intensidad

    if 'Intensidad' in df_coloreado.columns:

        def colorear_intensidad_val(x):

            try:

                val_lower = str(x).lower()

                if 'alta' in val_lower:

                    return f'<span style="color: #dc3545; font-weight: bold">{x}</span>'

                elif 'media' in val_lower:

                    return f'<span style="color: #fd7e14; font-weight: bold">{x}</span>'

                elif 'bajo' in val_lower or 'baja' in val_lower:

                    return f'<span style="color: #28a745; font-weight: bold">{x}</span>'

            except:

                pass

            return x

        

        df_coloreado['Intensidad'] = df_coloreado['Intensidad'].apply(colorear_intensidad_val)

    

    return df_coloreado



# Columnas que queremos mostrar

COLUMNAS_MOSTRAR = [

    'Agentes Zimach',

    'Sale Conv %',

    'Intensidad',

    'Meta S1',

    'Meta S2',

    'Meta S3',

    'Meta S4',

    'Impacto (%)\n(Conversión actual – Conversión semana anterior)',

    'Desviación (Conversión Real – Meta)'

]



COLUMNAS_COUCHING = [

    'Agentes Zimach',

    'Sale Conv %',

    'Acción Principal',

    'Detalle de Trabajo'

]



@st.cache_data

def cargar_datos():

    """Carga los datos del Excel"""

    excel_file = encuentra_archivo_excel('CONTROL DE AUDITORIAS.xlsx')

    if excel_file is None:

        st.warning("⚠️ No se encontró el archivo CONTROL DE AUDITORIAS.xlsx")

        return pd.DataFrame()

    df = pd.read_excel(excel_file, sheet_name='Data')

    

    # Seleccionar solo las columnas deseadas

    df_filtrado = df[COLUMNAS_MOSTRAR].copy()

    

    # Renombrar columnas para mejor legibilidad

    df_filtrado.columns = [

        'Agentes Zimach',

        'Sale Conv %',

        'Intensidad',

        'Meta S1',

        'Meta S2',

        'Meta S3',

        'Meta S4',

        'Impacto (%)',

        'Desviación'

    ]

    

    # Remover filas donde 'Agentes Zimach' sea NaN, vacío o etiquetas de resumen

    df_filtrado = df_filtrado.dropna(subset=['Agentes Zimach'])

    df_filtrado = df_filtrado[df_filtrado['Agentes Zimach'].astype(str).str.strip() != '']

    

    # Remover filas con etiquetas de resumen

    palabras_excluir = ['Total', 'Sale Conversion', 'total', 'sale conversion', 'nan']

    df_filtrado = df_filtrado[~df_filtrado['Agentes Zimach'].astype(str).str.contains('|'.join(palabras_excluir), case=False, na=False)]

    

    # Filtrar solo agentes Zimach

    df_filtrado = df_filtrado[df_filtrado['Agentes Zimach'].astype(str).str.contains('ZIM_', case=False, na=False)]

    

    # Filtrar usuarios ficticios

    usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']

    df_filtrado = df_filtrado[~df_filtrado['Agentes Zimach'].isin(usuarios_ficticios)]

    

    # Convertir columnas numéricas a porcentaje

    columnas_porcentaje = [

        'Sale Conv %',

        'Intensidad',

        'Meta S1',

        'Meta S2',

        'Meta S3',

        'Meta S4',

        'Impacto (%)',

        'Desviación'

    ]

    

    for col in columnas_porcentaje:

        if col in df_filtrado.columns:

            def format_porcentaje(x):

                try:

                    if pd.notna(x):

                        valor_str = str(x).strip()

                        if '%' in valor_str:

                            valor = float(valor_str.replace('%', ''))

                        else:

                            valor = float(valor_str) * 100

                        

                        valor_redondeado = round(valor, 2)

                        if valor_redondeado == int(valor_redondeado):

                            return f'{int(valor_redondeado)}%'

                        return f'{valor_redondeado:.2f}%'

                    return '-'

                except (ValueError, TypeError):

                    return str(x)

            

            df_filtrado[col] = df_filtrado[col].apply(format_porcentaje)

    

    return df_filtrado



@st.cache_data

def cargar_datos_couching():

    """Carga los datos de Couching del Excel"""

    excel_file = encuentra_archivo_excel('CONTROL DE AUDITORIAS.xlsx')

    if excel_file is None:

        st.warning("⚠️ No se encontró el archivo CONTROL DE AUDITORIAS.xlsx")

        return pd.DataFrame()

    df = pd.read_excel(excel_file, sheet_name='Couching')

    

    # Seleccionar solo las columnas deseadas

    df_filtrado = df[COLUMNAS_COUCHING].copy()

    

    # Renombrar columnas para mejor legibilidad

    df_filtrado.columns = [

        'Agentes Zimach',

        'Sale Conv %',

        'Acción Principal',

        'Detalle de Trabajo'

    ]

    

    # Remover filas donde 'Agentes Zimach' sea NaN, vacío o etiquetas de resumen

    df_filtrado = df_filtrado.dropna(subset=['Agentes Zimach'])

    df_filtrado = df_filtrado[df_filtrado['Agentes Zimach'].astype(str).str.strip() != '']

    

    # Remover filas con etiquetas de resumen y mantener solo agentes válidos

    palabras_excluir = ['Total', 'Sale Conversion', 'total', 'sale conversion', 'nan']

    df_filtrado = df_filtrado[~df_filtrado['Agentes Zimach'].astype(str).str.contains('|'.join(palabras_excluir), case=False, na=False)]

    

    # Filtrar solo agentes Zimach

    df_filtrado = df_filtrado[df_filtrado['Agentes Zimach'].astype(str).str.contains('ZIM_', case=False, na=False)]

    

    # Filtrar usuarios ficticios

    usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']

    df_filtrado = df_filtrado[~df_filtrado['Agentes Zimach'].isin(usuarios_ficticios)]

    

    # Convertir columnas numéricas a porcentaje (Sale Conv %)

    def format_porcentaje(x):

        try:

            if pd.notna(x):

                valor_str = str(x).strip()

                if '%' in valor_str:

                    valor = float(valor_str.replace('%', ''))

                else:

                    valor = float(valor_str) * 100

                

                valor_redondeado = round(valor, 2)

                if valor_redondeado == int(valor_redondeado):

                    return f'{int(valor_redondeado)}%'

                return f'{valor_redondeado:.2f}%'

            return '-'

        except (ValueError, TypeError):

            return str(x)

    

    df_filtrado['Sale Conv %'] = df_filtrado['Sale Conv %'].apply(format_porcentaje)

    

    return df_filtrado



@st.cache_data

def cargar_datos_metricas():

    """Carga y estructura los datos de la hoja Metricas"""

    excel_file = encuentra_archivo_excel('CONTROL DE AUDITORIAS.xlsx')

    if excel_file is None:

        return pd.DataFrame()

    

    # Mapeo manual de criterios con sus descripciones y puntajes

    metricas_datos = {

        'Presentaciòn': {

            'descripcion': 'Menciona su Nombre y Apellido. Resalta el nombre de la campaña, motivo de llamada e identificar al cliente.',

            'puntaje': 1,

            'segmento': 'Habilidades de Apertura'

        },

        'Expresion Verbal / Diccion ': {

            'descripcion': 'Energía/Fluidez/Tono de voz comercial/Vocabulario/Dirige al cliente con respeto',

            'puntaje': 4,

            'segmento': 'Habilidades de Apertura'

        },

        'Tiempo de Espera': {

            'descripcion': 'Justificar los tiempos, hacer buen uso de los tiempos',

            'puntaje': 3,

            'segmento': 'Habilidades de Apertura'

        },

        'Validación de titular / contacto correcto': {

            'descripcion': 'Evita pérdida de tiempo y mejora efectividad del contacto.',

            'puntaje': 2,

            'segmento': 'Habilidades de Apertura'

        },

        'Sondeo Asertivo ': {

            'descripcion': 'Busca detectar si hay interés o necesidad básica.',

            'puntaje': 5,

            'segmento': 'Habilidades de Apertura'

        },

        'Identificación de necesidad': {

            'descripcion': 'El asesor profundiza en la situación actual del cliente respecto a su servicio de internet.',

            'puntaje': 7,

            'segmento': 'Diagnóstico y Perfilamiento'

        },

        'Identificación de capacidad de pago / interés real': {

            'descripcion': 'El asesor valida si el cliente cuenta con capacidad económica e interés real para contratar.',

            'puntaje': 4,

            'segmento': 'Diagnóstico y Perfilamiento'

        },

        'Detección de decisor (titular o no)': {

            'descripcion': 'El asesor identifica si la persona es quien toma la decisión de contratación.',

            'puntaje': 4,

            'segmento': 'Diagnóstico y Perfilamiento'

        },

        'Escucha Activa': {

            'descripcion': 'Demuestra Escucha Activa y utiliza la información a su favor',

            'puntaje': 7,

            'segmento': 'Negociación'

        },

        'Manejo de llamada': {

            'descripcion': 'Mantiene el control de la llamada / Manejo de Objeción (generando al menos un intento adicional de retención)',

            'puntaje': 12,

            'segmento': 'Negociación'

        },

        'Seguridad ': {

            'descripcion': 'Transmite seguridad en la llamada',

            'puntaje': 5,

            'segmento': 'Negociación'

        },

        'Empatìa ': {

            'descripcion': 'Empatizar con el cliente/Actitud de Servicio',

            'puntaje': 8,

            'segmento': 'Negociación'

        },

        'Negocacion escalonada': {

            'descripcion': 'Ofrecer del plan mas alto al mas bajos con sus respectivos beneficios.',

            'puntaje': 8,

            'segmento': 'Negociación'

        },

        'Beneficios claros': {

            'descripcion': 'Comunicar de manera clara y orientada al cliente los beneficios del servicio.',

            'puntaje': 8,

            'segmento': 'Argumentación Comercial'

        },

        'Diferenciación vs competencia': {

            'descripcion': 'Destaca de forma clara por qué el servicio ofrecido es mejor o diferente frente a otras opciones.',

            'puntaje': 5,

            'segmento': 'Argumentación Comercial'

        },

        'Personalización del discurso según necesidad': {

            'descripcion': 'El asesor adapta su discurso comercial en función de la información obtenida.',

            'puntaje': 7,

            'segmento': 'Argumentación Comercial'

        },

        'Generación de urgencia': {

            'descripcion': 'Utilizar argumentos efectivos para convencer al cliente',

            'puntaje': 5,

            'segmento': 'Cierre de llamada'

        },

        'Registro correcto en sistema ': {

            'descripcion': 'Vicidial / Mantra - Registro correcto en el sistema',

            'puntaje': 3,

            'segmento': 'Cierre de llamada'

        },

        'Uso adecuado de etiquetas': {

            'descripcion': 'Etiquetar correctamente',

            'puntaje': 2,

            'segmento': 'Cierre de llamada'

        }

    }

    

    # Crear lista de datos

    datos_lista = []

    for criterio, info in metricas_datos.items():

        datos_lista.append({

            'Criterio': criterio.strip(),

            'Puntaje Máx.': info['puntaje'],

            'Descripción': info['descripcion'],

            'Segmento': info['segmento']

        })

    

    df_resultado = pd.DataFrame(datos_lista)

    df_resultado = df_resultado.sort_values(['Segmento', 'Criterio'])

    

    return df_resultado



@st.cache_data

def calcular_puntaje_desempeño():

    """Calcula el puntaje y porcentaje de desempeño para cada agente"""

    excel_file = encuentra_archivo_excel('CONTROL DE AUDITORIAS.xlsx')

    if excel_file is None:

        return pd.DataFrame()

    df_couching = pd.read_excel(excel_file, sheet_name='Couching')

    

    # Criterios evaluables

    criterios = [

        'Presentaciòn',

        'Expresion Verbal / Diccion ',

        'Tiempo de Espera',

        'Validación de titular / contacto correcto',

        'Sondeo Asertivo ',

        'Identificación de necesidad',

        'Identificación de capacidad de pago / interés real',

        'Detección de decisor (titular o no)',

        'Escucha Activa',

        'Manejo de llamada',

        'Seguridad ',

        'Empatìa ',

        'Negocacion escalonada',

        'Beneficios claros',

        'Diferenciación vs competencia',

        'Personalización del discurso según necesidad',

        'Generación de urgencia',

        'Registro correcto en sistema ',

        'Uso adecuado de etiquetas'

    ]

    

    puntos_por_criterio = {

        'Presentaciòn': 1,

        'Expresion Verbal / Diccion ': 4,

        'Tiempo de Espera': 3,

        'Validación de titular / contacto correcto': 2,

        'Sondeo Asertivo ': 5,

        'Identificación de necesidad': 7,

        'Identificación de capacidad de pago / interés real': 4,

        'Detección de decisor (titular o no)': 4,

        'Escucha Activa': 7,

        'Manejo de llamada': 12,

        'Seguridad ': 5,

        'Empatìa ': 8,

        'Negocacion escalonada': 8,

        'Beneficios claros': 8,

        'Diferenciación vs competencia': 5,

        'Personalización del discurso según necesidad': 7,

        'Generación de urgencia': 5,

        'Registro correcto en sistema ': 3,

        'Uso adecuado de etiquetas': 2

    }

    

    puntaje_maximo_total = sum(puntos_por_criterio.values())

    

    # Crear DataFrame con puntajes de desempeño

    resultados = []

    

    for idx, row in df_couching.iterrows():

        agente = row['Agentes Zimach']

        

        if pd.isna(agente) or str(agente).strip() == '':

            continue

        

        agente_str = str(agente).strip()

        

        if any(palabra in agente_str.lower() for palabra in ['total', 'sale conversion', 'nan']):

            continue

        

        if 'ZIM_' not in agente_str.upper():

            continue

        

        # Filtrar usuarios ficticios

        usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']

        if agente_str in usuarios_ficticios:

            continue

        

        # Calcular puntaje total del agente

        puntaje_total = 0

        for criterio in criterios:

            if criterio in row.index:

                valor = row[criterio]

                try:

                    if pd.notna(valor) and str(valor).lower() != 'n/a':

                        puntaje_total += float(valor)

                except (ValueError, TypeError):

                    pass

        

        # Calcular porcentaje

        porcentaje = (puntaje_total / puntaje_maximo_total * 100) if puntaje_maximo_total > 0 else 0

        

        resultados.append({

            'Agentes Zimach': agente,

            'Puntaje Total': int(puntaje_total) if puntaje_total == int(puntaje_total) else round(puntaje_total, 2),

            'Puntaje Máximo': puntaje_maximo_total,

            'Desempeño (%)': f'{porcentaje:.2f}%' if porcentaje != int(porcentaje) else f'{int(porcentaje)}%'

        })

    

    df_resultado = pd.DataFrame(resultados)

    return df_resultado



@st.cache_data

def cargar_datos_progreso():

    """Carga los datos de Progreso por Fecha del Excel"""

    try:

        excel_file = encuentra_archivo_excel('CONTROL DE AUDITORIAS.xlsx')

        if excel_file is None:

            return pd.DataFrame()

        df = pd.read_excel(excel_file, sheet_name='Progreso_Fecha')

        

        # Convertir columnas necesarias

        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

        

        # Renombrar % calidad a Calidad (%) si es necesario

        if '% calidad' in df.columns:

            df['Calidad (%)'] = (df['% calidad'] * 100).round(1)

        

        # Calcular/convertir semana del mes a número

        def extraer_numero_semana(x):

            """Extrae el número de semana de cualquier formato"""

            if pd.isna(x):

                return None

            # Si es string como "Semana 4", extrae el número

            if isinstance(x, str):

                import re

                match = re.search(r'\d+', x)

                if match:

                    return int(match.group())

            # Si es número, devuélvelo como int

            try:

                return int(x)

            except:

                pass

            return None

        

        # Si existe columna Semana, convertirla a número; si no, calcularla

        if 'Semana' in df.columns:

            df['Semana'] = df['Semana'].apply(extraer_numero_semana)

        else:

            df['Semana'] = df['Fecha'].dt.day.apply(lambda x: int((x-1)//7 + 1) if pd.notna(x) else None)

        

        # Ordena por agente y fecha para calcular progreso

        df = df.sort_values(['Agentes Zimach', 'Fecha'])

        

        # Calcular Δ vs anterior y Progreso

        df['% calidad anterior'] = df.groupby('Agentes Zimach')['Calidad (%)'].shift(1)

        df['Δ vs anterior'] = df['Calidad (%)'] - df['% calidad anterior']

        

        # Determinar progreso basado en la variación

        def obtener_progreso(row):

            if pd.isna(row['Δ vs anterior']):

                return '🟦 Línea base'

            elif row['Δ vs anterior'] >= 5:

                return '� Subiendo fuerte'

            elif 1 <= row['Δ vs anterior'] < 5:

                return '📈 Subiendo poquito'

            elif row['Δ vs anterior'] == 0:

                return '😌 Tranquilo'

            else:

                return '📉 Bajando'

        

        df['Progreso'] = df.apply(obtener_progreso, axis=1)

        

        # Formatear Δ vs anterior para mostrar

        df['Δ vs anterior_str'] = df['Δ vs anterior'].apply(

            lambda x: '-' if pd.isna(x) else (f'{x:+.1f}%' if x != 0 else '0%')

        )

        

        # Formatear Calidad (%) a porcentaje

        df['Calidad (%)_str'] = df['Calidad (%)'].apply(lambda x: f'{x:.1f}%' if pd.notna(x) else '-')

        

        # Filtrar usuarios ficticios

        usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP']

        df = df[~df['Agentes Zimach'].isin(usuarios_ficticios)]

        

        return df

    except Exception as e:

        st.warning(f"No se pudo cargar la hoja Progreso_Fecha: {str(e)}")

        return pd.DataFrame()



@st.cache_data

def procesar_datos_progreso(df_progreso):

    """Procesa datos de progreso (ya procesados en carga)"""

    if df_progreso.empty:

        return pd.DataFrame()

    return df_progreso.copy()



@st.cache_data

def generar_vista_semanal(df_progreso):

    """Genera vista semanal resumida de progreso"""

    if df_progreso.empty:

        return pd.DataFrame()

    

    try:

        df = df_progreso.copy()

        

        # Agrupar por agente y semana

        if 'Agentes Zimach' in df.columns and 'Semana' in df.columns and 'Calidad (%)' in df.columns:

            vista_semanal = df.groupby(['Agentes Zimach', 'Semana']).agg({

                'Calidad (%)': ['count', 'mean']

            }).reset_index()

            

            vista_semanal.columns = ['Agente', 'Semana', 'Evaluaciones', 'Prom. Calidad (%)']

            vista_semanal['Prom. Calidad (%)'] = vista_semanal['Prom. Calidad (%)'].round(1)

            vista_semanal['Evaluaciones'] = vista_semanal['Evaluaciones'].astype(int)

            

            # Calcular variación semanal

            vista_semanal = vista_semanal.sort_values(['Agente', 'Semana'])

            vista_semanal['Δ semanal (%)'] = vista_semanal.groupby('Agente')['Prom. Calidad (%)'].diff().round(2)

            vista_semanal['Δ es_primera'] = vista_semanal['Δ semanal (%)'].isna()

            vista_semanal['Δ semanal (%)'] = vista_semanal['Δ semanal (%)'].fillna(0)

            

            # Determinar estado con mejor diferenciación

            def obtener_estado(row):

                delta = row['Δ semanal (%)']

                es_primera = row['Δ es_primera']

                

                if es_primera:

                    return '⭐ Primera vez'

                elif delta >= 5:

                    return '📈 En Aumento'

                elif 1 <= delta < 5:

                    return '📈 Subiendo poquito'

                elif -1 < delta < 1 and delta != 0:

                    return '↔️ Mantiene Nivel'

                elif delta == 0:

                    return '😌 Tranquilo'

                else:

                    return '📉 Bajando'

            

            vista_semanal['Estado'] = vista_semanal.apply(obtener_estado, axis=1)

            

            return vista_semanal

    except Exception as e:

        st.warning(f"Error al procesar vista semanal: {str(e)}")

        return pd.DataFrame()



@st.cache_data

def calcular_resumen_progreso_agentes(df_progreso):

    """Calcula promedio de calidad, variación promedio y estado de progreso por agente"""

    if df_progreso.empty:

        return pd.DataFrame()

    

    try:

        resumen = []

        agentes_unicos = df_progreso['Agentes Zimach'].unique()

        

        for agente in agentes_unicos:

            df_agente = df_progreso[df_progreso['Agentes Zimach'] == agente]

            

            # Promedio de calidad

            prom_calidad = df_agente['Calidad (%)'].mean()

            

            # Delta promedio (solo deltas válidos, no NaN)

            deltas_validos = df_agente[df_agente['Δ vs anterior'].notna()]['Δ vs anterior'].values

            delta_promedio = deltas_validos.mean() if len(deltas_validos) > 0 else 0

            

            # Clasificación de progreso

            if delta_promedio >= 5:

                estado = '� Subiendo fuerte'

            elif 1 <= delta_promedio < 5:

                estado = '📈 En Aumento'

            elif -1 < delta_promedio <= 0:

                estado = '↔️ Mantiene Nivel'

            else:

                estado = '📉 En Disminución'

            

            resumen.append({

                'Agentes Zimach': agente,

                'Prom. Calidad': f'{prom_calidad:.1f}%',

                'Var. Progreso': f'{delta_promedio:+.2f}%',

                'Interpretación': estado

            })

        

        return pd.DataFrame(resumen)

    except Exception as e:

        return pd.DataFrame()



@st.cache_data
def cargar_datos_semanas():

    """Carga datos de calificación por semana"""

    excel_file_data = encuentra_archivo_excel('CONTROL DE AUDITORIAS.xlsx')
    excel_file_calidad = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')

    if excel_file_data is None or excel_file_calidad is None:

        return pd.DataFrame()

    

    try:

        # Leer datos de calidad
        df_cc = pd.read_excel(excel_file_calidad, sheet_name=0)
        
        # Filtrar registros sin agente
        df_cc = df_cc[df_cc['AGENTE'] != 'Sin agente'].copy()
        
        # Filtrar usuarios ficticios
        usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']
        df_cc = df_cc[~df_cc['AGENTE'].isin(usuarios_ficticios)].copy()
        
        # Parsear fecha con formato correcto
        df_cc['Fecha'] = pd.to_datetime(df_cc['Fecha'], format='%d/%m/%Y', errors='coerce')
        df_cc['Día'] = df_cc['Fecha'].dt.day
        
        # Función para asignar semana
        def asignar_semana(dia):
            if pd.isna(dia):
                return None
            dia = int(dia)
            if 1 <= dia <= 7:
                return 'S1'
            elif 8 <= dia <= 14:
                return 'S2'
            elif 15 <= dia <= 21:
                return 'S3'
            elif 22 <= dia <= 28:
                return 'S4'
            else:
                return 'S5'
        
        df_cc['Semana'] = df_cc['Día'].apply(asignar_semana)
        
        # Contar Sin Calificar por agente y semana
        df_sin = df_cc[df_cc['STATUS'] == 'SIN CALIFICAR'].copy()
        sin_por_semana = df_sin.groupby(['AGENTE', 'Semana']).size().reset_index(name='Sin_Calif')
        
        # Contar Exactitud (solo STATUS = 'EXACTITUD')
        df_exactitud = df_cc[df_cc['STATUS'] == 'EXACTITUD'].copy()
        exactitud_por_semana = df_exactitud.groupby(['AGENTE', 'Semana']).size().reset_index(name='Exactitud')
        
        # Merge sin y exactitud
        semanas_data = sin_por_semana.merge(exactitud_por_semana, on=['AGENTE', 'Semana'], how='outer')
        semanas_data = semanas_data.fillna(0).astype({'Sin_Calif': int, 'Exactitud': int})
        
        # Pivotar para cada tipo
        sin_pivot = semanas_data.pivot(index='AGENTE', columns='Semana', values='Sin_Calif').reset_index()
        exactitud_pivot = semanas_data.pivot(index='AGENTE', columns='Semana', values='Exactitud').reset_index()
        
        # Asegurar que todas las semanas existan (llenar con 0 si no hay datos)
        for semana in ['S1', 'S2', 'S3', 'S4', 'S5']:
            if semana not in sin_pivot.columns:
                sin_pivot[semana] = 0
            if semana not in exactitud_pivot.columns:
                exactitud_pivot[semana] = 0
        
        # Renombrar columnas semanas a Sin_S y Exactitud_S
        sin_pivot = sin_pivot.rename(columns={'S1': 'Sin_S1', 'S2': 'Sin_S2', 'S3': 'Sin_S3', 'S4': 'Sin_S4', 'S5': 'Sin_S5'})
        exactitud_pivot = exactitud_pivot.rename(columns={'S1': 'Exactitud_S1', 'S2': 'Exactitud_S2', 'S3': 'Exactitud_S3', 'S4': 'Exactitud_S4', 'S5': 'Exactitud_S5'})
        
        # Renombrar columna AGENTE a Agente
        sin_pivot.rename(columns={'AGENTE': 'Agente'}, inplace=True)
        exactitud_pivot.rename(columns={'AGENTE': 'Agente'}, inplace=True)
        
        # Merge sin y exactitud
        resultado = sin_pivot.merge(exactitud_pivot, on='Agente', how='outer')
        resultado = resultado.fillna(0)
        
        # Agregar Leads
        leads_count = df_cc['AGENTE'].value_counts().reset_index()
        leads_count.columns = ['Agente', 'Leads']
        resultado = resultado.merge(leads_count, on='Agente', how='left')
        resultado['Leads'] = resultado['Leads'].fillna(0).astype(int)
        
        # Reordenar columnas (Sin S1, Exactitud S1, Sin S2, Exactitud S2, ...)
        col_order = ['Agente', 'Leads']
        for i in range(1, 6):
            col_order.append(f'Sin_S{i}')
            col_order.append(f'Exactitud_S{i}')
        
        resultado = resultado[[col for col in col_order if col in resultado.columns]]
        resultado = resultado.sort_values('Agente').reset_index(drop=True)
        
        return resultado

    except Exception as e:
        st.error(f"Error al cargar datos de semanas: {str(e)}")
        return pd.DataFrame()



@st.cache_data

def cargar_datos_validacion_cobertura():
    """Carga datos de Validación de Cobertura y No Evaluado por agente"""
    try:
        excel_file = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')
        
        if excel_file is None:
            with st.spinner("📥 Descargando archivo de GitHub..."):
                excel_file = descargar_de_github('REPORTE CALIDAD.xlsx')
        
        if excel_file is None:
            return pd.DataFrame()
        
        df = pd.read_excel(excel_file, sheet_name=0)
        
        # Filtrar registros sin agente
        df = df[df['AGENTE'] != 'Sin agente'].copy()
        df = df.dropna(subset=['AGENTE'])
        
        # Filtrar usuarios ficticios
        usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']
        df = df[~df['AGENTE'].isin(usuarios_ficticios)].copy()
        
        # Contar total de leads por agente
        leads_por_agente = df['AGENTE'].value_counts().reset_index()
        leads_por_agente.columns = ['Agente', 'Total Leads']
        
        # Contar VALIDACION COBERTURA (STATUS = 'VALIDACION COBERTURA')
        df_validacion = df[df['STATUS'] == 'VALIDACION COBERTURA']
        validacion_por_agente = df_validacion['AGENTE'].value_counts().reset_index()
        validacion_por_agente.columns = ['Agente', 'Validacion Cobertura']
        
        # Contar NO EVALUADO (STATUS = NaN/vacío)
        df_no_evaluado = df[df['STATUS'].isna()]
        no_evaluado_por_agente = df_no_evaluado['AGENTE'].value_counts().reset_index()
        no_evaluado_por_agente.columns = ['Agente', 'No Evaluado']
        
        # Combinar datos
        resultado = leads_por_agente.copy()
        resultado = resultado.merge(validacion_por_agente, on='Agente', how='left')
        resultado = resultado.merge(no_evaluado_por_agente, on='Agente', how='left')
        
        # Llenar NaN con 0
        resultado['Validacion Cobertura'] = resultado['Validacion Cobertura'].fillna(0).astype(int)
        resultado['No Evaluado'] = resultado['No Evaluado'].fillna(0).astype(int)
        
        # Calcular porcentajes
        resultado['Validacion Cobertura %'] = (
            resultado['Validacion Cobertura'] / resultado['Total Leads'] * 100
        ).round(2)
        
        resultado['No Evaluado %'] = (
            resultado['No Evaluado'] / resultado['Total Leads'] * 100
        ).round(2)
        
        # Ordenar por Validación Cobertura descendente
        resultado = resultado.sort_values('Validacion Cobertura %', ascending=False).reset_index(drop=True)
        
        return resultado
    
    except Exception as e:
        st.error(f"Error al cargar datos de Validación de Cobertura: {str(e)}")
        return pd.DataFrame()


def cargar_datos_kpi():
    """Carga datos del Cumplimiento de KPI (Correctos) por agente"""
    try:
        excel_file = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')
        
        if excel_file is None:
            with st.spinner("📥 Descargando archivo de GitHub..."):
                excel_file = descargar_de_github('REPORTE CALIDAD.xlsx')
        
        if excel_file is None:
            return pd.DataFrame()
        
        df = pd.read_excel(excel_file, sheet_name=0)
        
        # Filtrar registros sin agente
        df = df[df['AGENTE'] != 'Sin agente'].copy()
        df = df.dropna(subset=['AGENTE'])
        
        # Filtrar usuarios ficticios
        usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']
        df = df[~df['AGENTE'].isin(usuarios_ficticios)].copy()
        
        # Contar total de leads por agente
        leads_por_agente = df['AGENTE'].value_counts().reset_index()
        leads_por_agente.columns = ['Agente', 'Total Leads']
        
        # Contar CORRECTO (STATUS = 'CORRECTO')
        df_correcto = df[df['STATUS'] == 'CORRECTO']
        correcto_por_agente = df_correcto['AGENTE'].value_counts().reset_index()
        correcto_por_agente.columns = ['Agente', 'Correcto']
        
        # Combinar datos
        resultado = leads_por_agente.copy()
        resultado = resultado.merge(correcto_por_agente, on='Agente', how='left')
        
        # Llenar NaN con 0
        resultado['Correcto'] = resultado['Correcto'].fillna(0).astype(int)
        
        # Calcular porcentaje de KPI
        resultado['KPI %'] = (
            resultado['Correcto'] / resultado['Total Leads'] * 100
        ).round(2)
        
        # Ordenar por KPI descendente
        resultado = resultado.sort_values('KPI %', ascending=False).reset_index(drop=True)
        
        return resultado
    
    except Exception as e:
        st.error(f"Error al cargar datos de KPI: {str(e)}")
        return pd.DataFrame()


def cargar_datos_control_calidad():

    """Carga los datos de Control de Calidad del archivo REPORTE CALIDAD.xlsx"""

    try:

        excel_file = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')

        

        if excel_file is None:

            # Intentar descargar de GitHub como última opción

            with st.spinner("📥 Descargando archivo de GitHub..."):

                excel_file = descargar_de_github('REPORTE CALIDAD.xlsx')

        

        if excel_file is None:

            # Mostrar información de depuración

            current_dir = os.getcwd()

            script_dir = os.path.dirname(os.path.abspath(__file__))

            

            error_msg = f"""

            ⚠️ No se encontró el archivo **REPORTE CALIDAD.xlsx**

            

            **Ubicaciones buscadas:**

            - {current_dir}

            - {script_dir}

            

            **Archivos disponibles en el directorio actual:**

            """

            

            try:

                files = [f for f in os.listdir(current_dir) if f.endswith('.xlsx')]

                if files:

                    for f in files:

                        error_msg += f"\n- {f}"

                else:

                    error_msg += "\n- (ningún archivo .xlsx encontrado)"

            except:

                pass

            

            st.warning(error_msg)

            return pd.DataFrame()

        

        df = pd.read_excel(excel_file, sheet_name=0)
        
        # Filtrar registros sin agente
        df = df[df['AGENTE'] != 'Sin agente'].copy()

        

        # Contar leads por agente

        leads_por_agente = df['AGENTE'].value_counts().reset_index()

        leads_por_agente.columns = ['Agente', 'Leads']

        

        # Contar SIN CALIFICAR

        df_sin_calificar = df[df['STATUS'] == 'SIN CALIFICAR']

        sin_calificar_por_agente = df_sin_calificar['AGENTE'].value_counts().reset_index()

        sin_calificar_por_agente.columns = ['Agente', 'Sin Calificar Q']

        

        # Contar EXACTITUD

        df_exactitud = df[df['STATUS'] == 'EXACTITUD']

        exactitud_por_agente = df_exactitud['AGENTE'].value_counts().reset_index()

        exactitud_por_agente.columns = ['Agente', 'Exactitud Q']

        

        # Combinar datos

        resultado = leads_por_agente.copy()

        resultado = resultado.merge(sin_calificar_por_agente, on='Agente', how='left')

        resultado = resultado.merge(exactitud_por_agente, on='Agente', how='left')

        

        # Llenar NaN con 0

        resultado['Sin Calificar Q'] = resultado['Sin Calificar Q'].fillna(0).astype(int)

        resultado['Exactitud Q'] = resultado['Exactitud Q'].fillna(0).astype(int)

        

        # Calcular porcentajes

        resultado['Sin Calificar %'] = (resultado['Sin Calificar Q'] / resultado['Leads'] * 100).round(2).astype(str) + '%'

        resultado['Exactitud %'] = (resultado['Exactitud Q'] / resultado['Leads'] * 100).round(2).astype(str) + '%'

        

        # Reordenar columnas

        resultado = resultado[['Agente', 'Leads', 'Sin Calificar Q', 'Sin Calificar %', 'Exactitud Q', 'Exactitud %']]

        

        # Ordenar por Agente

        resultado = resultado.sort_values('Agente').reset_index(drop=True)

        

        return resultado

    except Exception as e:

        st.error(f"Error al cargar datos de Control de Calidad: {str(e)}")

        return pd.DataFrame()


def cargar_datos_examen_bitel():
    """Carga datos del CONSOLIDADO EXAMEN BITEL.xlsx"""
    try:
        excel_file = encuentra_archivo_excel('CONSOLIDADO EXAMEN BITEL.xlsx')
        
        if excel_file is None:
            st.warning("⚠️ No se encontró el archivo **CONSOLIDADO EXAMEN BITEL.xlsx**")
            return pd.DataFrame()
        
        df = pd.read_excel(excel_file, sheet_name='Resultado_Examen_Calidad')
        
        # Limpiar espacios en nombres de columnas
        df.columns = df.columns.str.strip()
        
        # Convertir Fecha a datetime si es string
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        
        return df
    
    except Exception as e:
        st.error(f"Error al cargar datos de EXAMEN BITEL: {str(e)}")
        return pd.DataFrame()


def calcular_kpis_rendimiento_general(df):
    """Calcula KPIs de rendimiento general"""
    if df.empty:
        return {}
    
    try:
        # Promedio global de puntaje
        promedio_global = df['Puntaje de Evaluacion'].mean() if 'Puntaje de Evaluacion' in df.columns else 0
        
        # Porcentaje de aprobación
        total_evals = len(df)
        aprobados = len(df[df['Resultado'] == 'Aprobado']) if 'Resultado' in df.columns else 0
        pct_aprobacion = (aprobados / total_evals * 100) if total_evals > 0 else 0
        
        # Distribución por nivel
        distribucion_nivel = {}
        if 'Estado Puntaje' in df.columns:
            distribucion_nivel = df['Estado Puntaje'].value_counts().to_dict()
        
        # Promedio por tipo de examen
        promedio_por_tipo = {}
        if 'Tipo de Examen' in df.columns and 'Puntaje de Evaluacion' in df.columns:
            promedio_por_tipo = df.groupby('Tipo de Examen')['Puntaje de Evaluacion'].mean().to_dict()
        
        return {
            'promedio_global': promedio_global,
            'pct_aprobacion': pct_aprobacion,
            'total_evaluaciones': total_evals,
            'distribucion_nivel': distribucion_nivel,
            'promedio_por_tipo': promedio_por_tipo
        }
    except Exception as e:
        st.error(f"Error calculando KPIs de rendimiento: {str(e)}")
        return {}


def calcular_kpis_por_asesor(df):
    """Calcula KPIs por asesor"""
    if df.empty:
        return pd.DataFrame()
    
    try:
        resultado = []
        
        # Agrupar por empleado
        for empleado in df['Empleado'].unique():
            df_asesor = df[df['Empleado'] == empleado]
            
            # Cantidad de evaluaciones en nivel Bajo
            evals_bajo = len(df_asesor[df_asesor['Estado Puntaje'] == 'Bajo']) if 'Estado Puntaje' in df_asesor.columns else 0
            
            # Total de evaluaciones
            total_evals = len(df_asesor)
            
            # Promedio de puntaje
            promedio_puntaje = df_asesor['Puntaje de Evaluacion'].mean() if 'Puntaje de Evaluacion' in df_asesor.columns else 0
            
            # Porcentaje de aprobación
            aprobados = len(df_asesor[df_asesor['Resultado'] == 'Aprobado']) if 'Resultado' in df_asesor.columns else 0
            pct_aprobacion = (aprobados / total_evals * 100) if total_evals > 0 else 0
            
            resultado.append({
                'Asesor': empleado,
                'Total Evaluaciones': total_evals,
                'Evals Nivel Bajo': evals_bajo,
                'Promedio Puntaje': round(promedio_puntaje, 2),
                '% Aprobación': round(pct_aprobacion, 2),
                'Tiene Bajo': 'Sí' if evals_bajo > 0 else 'No'
            })
        
        return pd.DataFrame(resultado)
    
    except Exception as e:
        st.error(f"Error calculando KPIs por asesor: {str(e)}")
        return pd.DataFrame()


def calcular_kpis_temporales(df):
    """Calcula KPIs temporales agrupados por semana"""
    if df.empty:
        return {}
    
    try:
        # Volumen de evaluaciones realizadas
        total_evals = len(df)
        
        # Análisis por semana (si existe Fecha)
        evals_por_semana = {}
        if 'Fecha' in df.columns:
            # Agrupar por semana del año (formato: 2026-W12, etc)
            df_temp = df.copy()
            df_temp['Semana'] = df_temp['Fecha'].dt.strftime('%Y-W%V')
            evals_por_semana = df_temp.groupby('Semana').size().to_dict()
            # Ordenar las semanas
            evals_por_semana = dict(sorted(evals_por_semana.items()))
        
        # Promedio de evaluaciones por semana
        promedio_evals_semana = total_evals / len(evals_por_semana) if evals_por_semana else 0
        
        return {
            'total_evaluaciones': total_evals,
            'evals_por_semana': evals_por_semana,
            'promedio_evals_semana': promedio_evals_semana
        }
    except Exception as e:
        st.error(f"Error calculando KPIs temporales: {str(e)}")
        return {}


# Cargar datos

df_data = cargar_datos()

df_couching = cargar_datos_couching()

df_desempeño = calcular_puntaje_desempeño()

df_metricas = cargar_datos_metricas()

df_progreso = cargar_datos_progreso()

df_progreso_procesado = procesar_datos_progreso(df_progreso)

df_vista_semanal = generar_vista_semanal(df_progreso_procesado)

df_resumen_progreso = calcular_resumen_progreso_agentes(df_progreso_procesado)

df_control_calidad = cargar_datos_control_calidad()

df_validacion_cobertura = cargar_datos_validacion_cobertura()

df_semanas = cargar_datos_semanas()

df_examen_bitel = cargar_datos_examen_bitel()


# ✅ FILTRO DE USUARIOS FICTICIOS
# Lista de usuarios ficticios a excluir
usuarios_ficticios = [
    'ZIM_FLAVIOZM_VTP',
    'ZIM_KATHERINEMM_VTP',
    'ZIM_CARLOSVG_VTP',
    'ZIM_ANTHONYJR_VTP'
]

# Aplicar filtro a todos los DataFrames que contienen información de agentes
if not df_control_calidad.empty and 'Agente' in df_control_calidad.columns:
    df_control_calidad = df_control_calidad[~df_control_calidad['Agente'].isin(usuarios_ficticios)].reset_index(drop=True)

if not df_validacion_cobertura.empty and 'Agente' in df_validacion_cobertura.columns:
    df_validacion_cobertura = df_validacion_cobertura[~df_validacion_cobertura['Agente'].isin(usuarios_ficticios)].reset_index(drop=True)

if not df_data.empty and 'Agentes Zimach' in df_data.columns:
    df_data = df_data[~df_data['Agentes Zimach'].isin(usuarios_ficticios)].reset_index(drop=True)

if not df_couching.empty and 'Agentes Zimach' in df_couching.columns:
    df_couching = df_couching[~df_couching['Agentes Zimach'].isin(usuarios_ficticios)].reset_index(drop=True)


# ✅ FILTRO POR MES - REPORTE CALIDAD
# Extraer meses disponibles de REPORTE CALIDAD.xlsx
excel_file_calidad = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')
meses_disponibles = []
mes_filtro_global = None
mes_numero_filtro = None
año_filtro = None

if excel_file_calidad:
    try:
        df_calidad_fechas = pd.read_excel(excel_file_calidad, sheet_name=0)
        # Convertir columna Fecha a datetime (formato DD/MM/YYYY)
        if 'Fecha' in df_calidad_fechas.columns:
            df_calidad_fechas['Fecha'] = pd.to_datetime(df_calidad_fechas['Fecha'], format='%d/%m/%Y', errors='coerce')
            df_calidad_fechas['Mes_Texto'] = df_calidad_fechas['Fecha'].dt.strftime('%m/%Y')  # MM/YYYY
            df_calidad_fechas['Mes_Num'] = df_calidad_fechas['Fecha'].dt.month
            df_calidad_fechas['Año'] = df_calidad_fechas['Fecha'].dt.year
            # Obtener meses únicos y ordenarlos (más recientes primero)
            meses_unicos = df_calidad_fechas[['Mes_Texto', 'Mes_Num', 'Año']].drop_duplicates()
            meses_unicos = meses_unicos.sort_values(['Año', 'Mes_Num'], ascending=[False, False])
            meses_disponibles = meses_unicos['Mes_Texto'].tolist()
    except Exception as e:
        st.warning(f"Error al procesar fechas de REPORTE CALIDAD: {str(e)}")

# --- Mostrar selector de mes (UI)
st.markdown("## 📊 Dashboard - Control de Auditorías")
st.markdown("*Análisis de desempeño de agentes y métricas de calidad*")

col_filtro, col_info = st.columns([3, 6])

with col_filtro:
    if meses_disponibles:
        mes_filtro_global = st.selectbox("📅 **Filtrar por mes (MM/YYYY):**", meses_disponibles, index=0, key="filtro_mes_global")
        # Extraer mes y año del filtro seleccionado
        if mes_filtro_global:
            parts = mes_filtro_global.split('/')
            mes_numero_filtro = int(parts[0])
            año_filtro = int(parts[1])
    else:
        st.info("No hay datos de fechas disponibles")

# Aplicar filtro de mes SOLO a datos de REPORTE CALIDAD
if mes_filtro_global and mes_numero_filtro and año_filtro:
    # Filtrar datos de semanas (de REPORTE CALIDAD)
    if not df_semanas.empty and 'Agente' in df_semanas.columns:
        try:
            # Recargar df_semanas filtrado por mes
            excel_file_data = encuentra_archivo_excel('CONTROL DE AUDITORIAS.xlsx')
            excel_file_cal = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')
            if excel_file_data and excel_file_cal:
                df_cc = pd.read_excel(excel_file_cal, sheet_name=0)
                df_cc = df_cc[df_cc['AGENTE'] != 'Sin agente'].copy()
                df_cc['Fecha'] = pd.to_datetime(df_cc['Fecha'], format='%d/%m/%Y', errors='coerce')
                df_cc['Día'] = df_cc['Fecha'].dt.day
                df_cc['Mes'] = df_cc['Fecha'].dt.month
                df_cc['Año'] = df_cc['Fecha'].dt.year
                
                # Filtrar por mes y año
                df_cc = df_cc[(df_cc['Mes'] == mes_numero_filtro) & (df_cc['Año'] == año_filtro)].copy()
                
                # Filtrar usuarios ficticios
                usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']
                df_cc = df_cc[~df_cc['AGENTE'].isin(usuarios_ficticios)].copy()
                
                # Función para asignar semana
                def asignar_semana(dia):
                    if dia <= 7:
                        return 'S1'
                    elif dia <= 14:
                        return 'S2'
                    elif dia <= 21:
                        return 'S3'
                    elif dia <= 28:
                        return 'S4'
                    else:
                        return 'S5'
                
                df_cc['Semana'] = df_cc['Día'].apply(asignar_semana)
                
                # Contar Sin Calificar por agente y semana
                df_sin = df_cc[df_cc['STATUS'] == 'SIN CALIFICAR'].copy()
                sin_por_semana = df_sin.groupby(['AGENTE', 'Semana']).size().reset_index(name='Sin_Calif')
                
                # Contar Exactitud
                df_exactitud = df_cc[df_cc['STATUS'] == 'EXACTITUD'].copy()
                exactitud_por_semana = df_exactitud.groupby(['AGENTE', 'Semana']).size().reset_index(name='Exactitud')
                
                # Merge
                semanas_data = sin_por_semana.merge(exactitud_por_semana, on=['AGENTE', 'Semana'], how='outer')
                semanas_data = semanas_data.fillna(0).astype({'Sin_Calif': int, 'Exactitud': int})
                
                # Pivotar
                sin_pivot = semanas_data.pivot(index='AGENTE', columns='Semana', values='Sin_Calif').reset_index()
                exactitud_pivot = semanas_data.pivot(index='AGENTE', columns='Semana', values='Exactitud').reset_index()
                
                # Asegurar semanas
                for semana in ['S1', 'S2', 'S3', 'S4', 'S5']:
                    if semana not in sin_pivot.columns:
                        sin_pivot[semana] = 0
                    if semana not in exactitud_pivot.columns:
                        exactitud_pivot[semana] = 0
                
                sin_pivot = sin_pivot.rename(columns={'S1': 'Sin_S1', 'S2': 'Sin_S2', 'S3': 'Sin_S3', 'S4': 'Sin_S4', 'S5': 'Sin_S5'})
                exactitud_pivot = exactitud_pivot.rename(columns={'S1': 'Exactitud_S1', 'S2': 'Exactitud_S2', 'S3': 'Exactitud_S3', 'S4': 'Exactitud_S4', 'S5': 'Exactitud_S5'})
                
                sin_pivot.rename(columns={'AGENTE': 'Agente'}, inplace=True)
                exactitud_pivot.rename(columns={'AGENTE': 'Agente'}, inplace=True)
                
                df_semanas = sin_pivot.merge(exactitud_pivot, on='Agente', how='outer').fillna(0)
                leads_count = df_cc['AGENTE'].value_counts().reset_index()
                leads_count.columns = ['Agente', 'Leads']
                df_semanas = df_semanas.merge(leads_count, on='Agente', how='left').fillna(0)
        except:
            pass
    
    # Filtrar datos de control de calidad (REPORTE CALIDAD)
    if not df_control_calidad.empty and 'Agente' in df_control_calidad.columns:
        try:
            excel_file = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')
            if excel_file:
                df = pd.read_excel(excel_file, sheet_name=0)
                df = df[df['AGENTE'] != 'Sin agente'].copy()
                df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
                df['Mes'] = df['Fecha'].dt.month
                df['Año'] = df['Fecha'].dt.year
                df = df[(df['Mes'] == mes_numero_filtro) & (df['Año'] == año_filtro)].copy()
                
                # Filtrar usuarios ficticios
                usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']
                df = df[~df['AGENTE'].isin(usuarios_ficticios)].copy()
                
                leads_por_agente = df['AGENTE'].value_counts().reset_index()
                leads_por_agente.columns = ['Agente', 'Leads']
                
                df_sin_calificar = df[df['STATUS'] == 'SIN CALIFICAR']
                sin_calificar_por_agente = df_sin_calificar['AGENTE'].value_counts().reset_index()
                sin_calificar_por_agente.columns = ['Agente', 'Sin Calificar Q']
                
                df_exactitud = df[df['STATUS'] == 'EXACTITUD']
                exactitud_por_agente = df_exactitud['AGENTE'].value_counts().reset_index()
                exactitud_por_agente.columns = ['Agente', 'Exactitud Q']
                
                resultado = leads_por_agente.copy()
                resultado = resultado.merge(sin_calificar_por_agente, on='Agente', how='left')
                resultado = resultado.merge(exactitud_por_agente, on='Agente', how='left')
                resultado['Sin Calificar Q'] = resultado['Sin Calificar Q'].fillna(0).astype(int)
                resultado['Exactitud Q'] = resultado['Exactitud Q'].fillna(0).astype(int)
                resultado['Sin Calificar %'] = (resultado['Sin Calificar Q'] / resultado['Leads'] * 100).round(2).astype(str) + '%'
                resultado['Exactitud %'] = (resultado['Exactitud Q'] / resultado['Leads'] * 100).round(2).astype(str) + '%'
                resultado = resultado[['Agente', 'Leads', 'Sin Calificar Q', 'Sin Calificar %', 'Exactitud Q', 'Exactitud %']]
                resultado = resultado.sort_values('Agente').reset_index(drop=True)
                df_control_calidad = resultado
        except:
            pass
    
    # Filtrar datos de validación de cobertura (REPORTE CALIDAD)
    if not df_validacion_cobertura.empty and 'Agente' in df_validacion_cobertura.columns:
        try:
            excel_file = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')
            if excel_file:
                df = pd.read_excel(excel_file, sheet_name=0)
                df = df[df['AGENTE'] != 'Sin agente'].copy()
                df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
                df['Mes'] = df['Fecha'].dt.month
                df['Año'] = df['Fecha'].dt.year
                df = df[(df['Mes'] == mes_numero_filtro) & (df['Año'] == año_filtro)].copy()
                
                # Filtrar usuarios ficticios
                usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']
                df = df[~df['AGENTE'].isin(usuarios_ficticios)].copy()
                
                leads_por_agente = df['AGENTE'].value_counts().reset_index()
                leads_por_agente.columns = ['Agente', 'Total Leads']
                
                df_validacion = df[df['STATUS'] == 'VALIDACION COBERTURA']
                validacion_por_agente = df_validacion['AGENTE'].value_counts().reset_index()
                validacion_por_agente.columns = ['Agente', 'Validacion Cobertura']
                
                df_no_evaluado = df[df['STATUS'].isna()]
                no_evaluado_por_agente = df_no_evaluado['AGENTE'].value_counts().reset_index()
                no_evaluado_por_agente.columns = ['Agente', 'No Evaluado']
                
                resultado = leads_por_agente.copy()
                resultado = resultado.merge(validacion_por_agente, on='Agente', how='left')
                resultado = resultado.merge(no_evaluado_por_agente, on='Agente', how='left')
                resultado['Validacion Cobertura'] = resultado['Validacion Cobertura'].fillna(0).astype(int)
                resultado['No Evaluado'] = resultado['No Evaluado'].fillna(0).astype(int)
                resultado['Validacion Cobertura %'] = (resultado['Validacion Cobertura'] / resultado['Total Leads'] * 100).round(2)
                resultado['No Evaluado %'] = (resultado['No Evaluado'] / resultado['Total Leads'] * 100).round(2)
                resultado = resultado.sort_values('Validacion Cobertura %', ascending=False).reset_index(drop=True)
                df_validacion_cobertura = resultado
        except:
            pass
    
    # Mostrar información del filtro
    with col_info:
        st.success(f"📅 Datos de REPORTE CALIDAD filtrados por: **{mes_filtro_global}**")

st.markdown("---")


# Cálculos para estadísticas
excel_file = encuentra_archivo_excel('CONTROL DE AUDITORIAS.xlsx')
if excel_file:
    df_raw = pd.read_excel(excel_file, sheet_name='Data')
    df_raw_filtrado = df_raw[df_raw['Agentes Zimach'].astype(str).str.contains('ZIM_', case=False, na=False)]
    
    # Filtrar usuarios ficticios
    usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']
    df_raw_filtrado = df_raw_filtrado[~df_raw_filtrado['Agentes Zimach'].isin(usuarios_ficticios)].copy()
    
    total_agentes = len(df_raw_filtrado)
    
    # Convertir Sale Conv % a número (eliminar % si es string)
    try:
        if 'Sale Conv %' in df_raw_filtrado.columns:
            conv_valores = df_raw_filtrado['Sale Conv %'].apply(
                lambda x: float(str(x).replace('%', '')) if pd.notna(x) else 0
            )
            conv_promedio = conv_valores.mean()
        else:
            conv_promedio = 0
    except:
        conv_promedio = 0
    
    # Calcular calidad promedio
    try:
        if '% calidad' in df_raw_filtrado.columns:
            calidad_valores = df_raw_filtrado['% calidad'].apply(
                lambda x: float(str(x).replace('%', '')) if pd.notna(x) else 0
            )
            calidad_promedio = calidad_valores.mean()
        else:
            calidad_promedio = 0
    except:
        calidad_promedio = 0
else:
    total_agentes = 0
    conv_promedio = 0


# Verificar archivos necesarios

archivos_requeridos = ['CONTROL DE AUDITORIAS.xlsx', 'REPORTE CALIDAD.xlsx']

archivos_encontrados = []

archivos_faltantes = []



for archivo in archivos_requeridos:

    ruta = encuentra_archivo_excel(archivo)

    if ruta:

        archivos_encontrados.append(archivo)

    else:

        archivos_faltantes.append(archivo)



if archivos_faltantes:

    with st.expander("⚠️ Archivos faltantes", expanded=False):

        st.warning(f"Se necesita el archivo: **{', '.join(archivos_faltantes)}**")

        st.info(f"✅ Archivos encontrados: {len(archivos_encontrados)}\n\n❌ Archivos faltantes: {len(archivos_faltantes)}")



# Tabs para diferentes vistas

# Tabs principales: Monitoreo y Control de Calidad

tab_monitoreo, tab_control_calidad = st.tabs(

    ["📊 Monitoreo", "📊 Control de Calidad"]

)



# ==============================================

# TAB MONITOREO

# ==============================================

with tab_monitoreo:

    # Métricas principales de Monitoreo
    st.markdown("### 📊 Indicadores Principales")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">👥 Total de Agentes</div>
                <div style="font-size: 2.5rem; font-weight: bold; margin: 10px 0;">{int(total_agentes)}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.write(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">↔️ Conversión Promedio</div>
                <div style="font-size: 2.5rem; font-weight: bold; margin: 10px 0;">{conv_promedio * 100:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.write(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">⭐ Calidad Promedio</div>
                <div style="font-size: 2.5rem; font-weight: bold; margin: 10px 0;">{calidad_promedio * 100:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Subtabs dentro de Monitoreo

    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6, subtab7 = st.tabs(

        ["📋 Control de Auditorias", "📋 Plan de Acción", "📈 Progreso de Plan", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad"]

    )



    # SubTab 1: Datos de Control

    with subtab1:

        st.write("<h2 style='text-align: center;'>📋 Control de Auditorías</h2>", unsafe_allow_html=True)

        # Combinar datos de control con resumen de progreso

        df_control_mejorado = df_data.copy()

    

        # Hacer merge con el resumen de progreso

        if not df_resumen_progreso.empty:

            df_control_mejorado = df_control_mejorado.merge(

                df_resumen_progreso[['Agentes Zimach', 'Prom. Calidad', 'Var. Progreso', 'Interpretación']],

                on='Agentes Zimach',

                how='left'

            )

        

            # Reordenar columnas para que Prom. Calidad esté en lugar de % Calidad

            if 'Sale Conv %' in df_control_mejorado.columns:

                columnas_nuevo_orden = ['Agentes Zimach', 'Sale Conv %', 'Prom. Calidad', 'Var. Progreso', 'Interpretación']

            

                # Agregar el resto de columnas que no estén en el nuevo orden

                resto_columnas = [col for col in df_control_mejorado.columns if col not in columnas_nuevo_orden]

                columnas_final = columnas_nuevo_orden + resto_columnas

            

                # Mantener solo las columnas que existan

                columnas_final = [col for col in columnas_final if col in df_control_mejorado.columns]

                df_control_mejorado = df_control_mejorado[columnas_final]

    

        # Ajustar índice para que empiece desde 1
        df_control_mejorado.index = df_control_mejorado.index + 1
        
        # Mostrar tabla como dataframe nativo de Streamlit
        st.dataframe(df_control_mejorado, use_container_width=True, height=400)

    

        # Descargar datos

        csv_data = df_control_mejorado.to_csv(index=False).encode('utf-8')

        st.download_button(

            label="📥 Descargar Control en CSV",

            data=csv_data,

            file_name=f"control_datos_{datetime.now().strftime('%Y%m%d')}.csv",

            mime="text/csv"

        )



    # SubTab 2: Plan de Acción

    with subtab2:

        st.write("<h2 style='text-align: center;'>📋 Plan de Acción</h2>", unsafe_allow_html=True)

        df_couching.index = df_couching.index + 1
        st.dataframe(df_couching, width='stretch', height=400)

    

        csv_couching = df_couching.to_csv(index=False).encode('utf-8')

        st.download_button(

            label="📥 Descargar Plan de Acción en CSV",

            data=csv_couching,

            file_name=f"plan_accion_{datetime.now().strftime('%Y%m%d')}.csv",

            mime="text/csv"

        )



    # SubTab 3: Progreso de Plan

    with subtab3:

        st.write("<h2 style='text-align: center;'>📈 Progreso de Plan - Evolución de Desempeño</h2>", unsafe_allow_html=True)

    

        if df_progreso.empty:

            st.warning("⚠️ No se encontraron datos en la hoja 'Progreso_Fecha'. Asegúrate de que la hoja existe y contiene datos.")

        else:

            # Crear pestañas dentro de tab3

            tab3_diaria, tab3_semanal = st.tabs(["📅 Vista Diaria", "📈 Vista Semanal"])

        

            # Vista Diaria

            with tab3_diaria:

                st.subheader("Evolución Diaria de Calidad")

            

                # Seleccionar agente

                agentes_disponibles = sorted(df_progreso['Agentes Zimach'].unique()) if 'Agentes Zimach' in df_progreso.columns else []

            

                if agentes_disponibles:

                    agente_seleccionado = st.selectbox("Selecciona un agente:", agentes_disponibles, key="agente_progreso_diaria")

                

                    # Filtrar datos del agente

                    df_agente = df_progreso[df_progreso['Agentes Zimach'] == agente_seleccionado].copy()

                

                    if not df_agente.empty:

                        # Crear tabla HTML mejorada

                        html_diaria = '<style>.tabla-progreso-diaria { width: 100%; border-collapse: collapse; margin: 15px 0; } .tabla-progreso-diaria thead { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; } .tabla-progreso-diaria th { padding: 12px; text-align: center; font-weight: bold; } .tabla-progreso-diaria td { padding: 12px; border-bottom: 1px solid #ddd; text-align: center; } .tabla-progreso-diaria tbody tr:hover { background-color: #f5f5f5; } .mejora { color: #28a745; font-weight: bold; } .sin-cambio { color: #6c757d; } .decremento { color: #dc3545; font-weight: bold; } .baseline { color: #fd7e14; font-weight: bold; }</style><table class="tabla-progreso-diaria"><thead><tr><th>📅 Fecha</th><th>📊 Semana</th><th>% Calidad</th><th>Δ vs anterior</th><th>Estado de Progreso</th></tr></thead><tbody>'

                    

                        for idx, row in df_agente.iterrows():

                            fecha = row['Fecha'].strftime('%d/%m/%Y') if pd.notna(row['Fecha']) else '-'

                            semana = str(row['Semana']) if pd.notna(row['Semana']) else '-'

                            calidad = str(row['Calidad (%)_str']) if pd.notna(row['Calidad (%)_str']) else '-'

                            delta = str(row['Δ vs anterior_str']) if pd.notna(row['Δ vs anterior_str']) else '-'

                            progreso = str(row['Progreso']) if pd.notna(row['Progreso']) else '-'

                        

                            # Determinar clase CSS para delta

                            if delta == '-' or delta == 'Sin cambio':

                                clase_delta = 'baseline'

                            elif float(row['Δ vs anterior']) > 0 if pd.notna(row['Δ vs anterior']) else False:

                                clase_delta = 'mejora'

                            elif delta == '0%' or row['Δ vs anterior'] == 0:

                                clase_delta = 'sin-cambio'

                            else:

                                clase_delta = 'decremento'

                        

                            html_diaria += f'<tr><td>{fecha}</td><td><strong>{semana}</strong></td><td><strong>{calidad}</strong></td><td class="{clase_delta}">{delta}</td><td>{progreso}</td></tr>'

                    

                        html_diaria += '</tbody></table>'

                        st.markdown(html_diaria, unsafe_allow_html=True)

                    

                        # Gráfico de evolución

                        if 'Calidad (%)' in df_agente.columns and 'Fecha' in df_agente.columns:

                            st.subheader("Gráfico de Evolución")

                        

                            # Crear gráfico

                            import altair as alt

                        

                            chart = alt.Chart(df_agente).mark_line(point=True, color='#667eea', size=3).encode(

                                x=alt.X('Fecha:O', title='Fecha'),

                                y=alt.Y('Calidad (%):Q', title='% Calidad', scale=alt.Scale(domain=[0, 100])),

                                tooltip=['Fecha:O', 'Calidad (%):Q']

                            ).properties(

                                width=600,

                                height=300,

                                title='Evolución de Calidad del Agente'

                            )

                        

                            st.altair_chart(chart, use_container_width=True)

                        else:

                            st.info(f"No hay datos disponibles para {agente_seleccionado}")

                    else:

                        st.info(f"No hay datos disponibles para {agente_seleccionado}")

                else:

                    st.warning("No se encontraron agentes con datos de progreso")

        

            # Vista Semanal

            with tab3_semanal:

                st.subheader("Resumen Semanal de Desempeño")

            

                if not df_vista_semanal.empty:

                    st.markdown("### 📋 Haz clic para ver detalles diarios de cada agente")

                

                    # Crear expanders para cada agente de la vista semanal

                    agentes_unicos = df_vista_semanal['Agente'].unique()

                

                    for agente in sorted(agentes_unicos):

                        with st.expander(f"👤 {agente} - Ver evaluaciones diarias"):

                            df_agente_diario = df_progreso[df_progreso['Agentes Zimach'] == agente].copy()

                        

                            if not df_agente_diario.empty:

                                # Tabla de evaluaciones diarias

                                html_diario = '<style>.tabla-diario { width: 100%; border-collapse: collapse; margin: 10px 0; } .tabla-diario thead { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; } .tabla-diario th { padding: 10px; text-align: center; font-size: 12px; } .tabla-diario td { padding: 10px; border-bottom: 1px solid #ddd; text-align: center; font-size: 13px; } .tabla-diario tbody tr:hover { background-color: #f9f9f9; } .mejora { color: #28a745; font-weight: bold; } .estable { color: #6c757d; } .decremento { color: #dc3545; font-weight: bold; } .primera { color: #0dcaf0; font-weight: bold; } .agente-dia { text-align: left; font-weight: 500; }</style><table class="tabla-diario"><thead><tr><th>📅 Fecha</th><th>📊 Semana</th><th>% Calidad</th><th>Δ vs día anterior</th><th>Cambio (aumento/disminución)</th><th>Nota</th></tr></thead><tbody>'

                            

                                for idx, row in df_agente_diario.iterrows():

                                    fecha = row['Fecha'].strftime('%d/%m/%Y') if pd.notna(row['Fecha']) else '-'

                                    semana = f"Semana {int(row['Semana'])}" if pd.notna(row['Semana']) else '-'

                                    calidad = f"{row['Calidad (%)']:.1f}%" if pd.notna(row['Calidad (%)']) else '-'

                                    delta = row['Δ vs anterior'] if pd.notna(row['Δ vs anterior']) else 0

                                    delta_str = f"{delta:+.2f}%" if delta != 0 else "Sin cambio"

                                

                                    # Determine la clase y nota

                                    if pd.isna(row['Δ vs anterior']):

                                        clase = 'primera'

                                        nota = '⭐ Primera evaluación'

                                    elif delta > 0:

                                        clase = 'mejora'

                                        nota = f'✅ Mejoró {delta:.2f}%'

                                    elif delta == 0:

                                        clase = 'estable'

                                        nota = '➡️ Mantiene nivel'

                                    else:

                                        clase = 'decremento'

                                        nota = f'⚠️ Bajó {abs(delta):.2f}%'

                                

                                    html_diario += f'<tr><td>{fecha}</td><td>{semana}</td><td><strong>{calidad}</strong></td><td class="{clase}"><strong>{delta_str}</strong></td><td class="{clase}">{delta_str}</td><td>{nota}</td></tr>'

                            

                                html_diario += '</tbody></table>'

                                st.markdown(html_diario, unsafe_allow_html=True)

                            

                                # Estadísticas del agente

                                col1, col2, col3, col4 = st.columns(4)

                                with col1:

                                    st.metric("📊 Total Evaluaciones", len(df_agente_diario))

                                with col2:

                                    prom = df_agente_diario['Calidad (%)'].mean()

                                    st.metric("📈 Promedio General", f"{prom:.1f}%")

                                with col3:

                                    max_cal = df_agente_diario['Calidad (%)'].max()

                                    st.metric("⬆️ Máximo Alcanzado", f"{max_cal:.1f}%")

                                with col4:

                                    min_cal = df_agente_diario['Calidad (%)'].min()

                                    st.metric("⬇️ Mínimo Registrado", f"{min_cal:.1f}%")

                            

                                # Calcular delta promedio para interpretar el resultado

                                deltas_validos = df_agente_diario[df_agente_diario['Δ vs anterior'].notna()]['Δ vs anterior'].values

                            

                                if len(deltas_validos) > 0:

                                    delta_promedio = deltas_validos.mean()

                                

                                    # Determinar clasificación y mostrar recomendación

                                    if delta_promedio >= 5:

                                        color_bg = "#d4edda"

                                        color_border = "#28a745"

                                        icono = "�"

                                        titulo = "En Aumento"

                                        recomendacion = f"¡Excelente! {agente} está demostrando un incremento sostenido de <strong>+{delta_promedio:.2f}%</strong> en su desempeño. Continúa con las estrategias actuales de coaching. Se recomienda evaluar qué está funcionando bien y replicarlo en otras áreas."

                                    elif 1 <= delta_promedio < 5:

                                        color_bg = "#fff3cd"

                                        color_border = "#ffc107"

                                        icono = "�"

                                        titulo = "En Aumento"

                                        recomendacion = f"{agente} está avanzando con una mejora leve de <strong>+{delta_promedio:.2f}%</strong>. Se recomienda intensificar el coaching enfocándose en las áreas críticas. Realiza feedback más frecuentes y establece objetivos más claros."

                                    elif -1 < delta_promedio <= 0:

                                        color_bg = "#f8f9fa"

                                        color_border = "#6c757d"

                                        icono = "😌"

                                        titulo = "Mantiene Nivel"

                                        recomendacion = f"{agente} está manteniendo su nivel con cambios mínimos de <strong>{delta_promedio:.2f}%</strong>. Analiza si necesita más apoyo o nuevas estrategias de coaching para generar impulso."

                                    else:

                                        color_bg = "#f8d7da"

                                        color_border = "#dc3545"

                                        icono = "�"

                                        titulo = "En Disminución"

                                        recomendacion = f"{agente} está bajando con un decremento de <strong>{delta_promedio:.2f}%</strong>. Se requiere intervención inmediata. Realiza una evaluación profunda de barreras, aumenta la frecuencia de coaching y considera coaching intensivo."

                                

                                    st.markdown(f"""

                                    <div style="background: {color_bg}; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid {color_border};">

                                    <h3 style="margin-top: 0; color: #2c3e50;">{icono} {titulo}</h3>

                                    <p style="margin: 10px 0; color: #34495e; font-size: 16px;">{recomendacion}</p>

                                    </div>

                                    """, unsafe_allow_html=True)

                                else:

                                    st.info("⏳ Se necesitan al menos 2 evaluaciones para calcular el progreso.")

                            

                                # Gráfico de evolución

                                st.subheader("📉 Gráfico de Evolución")

                                import altair as alt

                            

                                chart = alt.Chart(df_agente_diario).mark_line(point=True, color='#667eea', size=3).encode(

                                    x=alt.X('Fecha:O', title='Fecha'),

                                    y=alt.Y('Calidad (%):Q', title='% Calidad', scale=alt.Scale(domain=[0, 100])),

                                    tooltip=['Fecha:O', 'Calidad (%):Q', 'Δ vs anterior:Q']

                                ).properties(

                                    height=300,

                                    title=f'Evolución de {agente}'

                                )

                            

                                st.altair_chart(chart, use_container_width=True)

                

                    st.markdown("---")

                    # Descarga de datos

                    csv_vista_semanal = df_vista_semanal.to_csv(index=False).encode('utf-8')

                    st.download_button(

                        label="📥 Descargar Vista Semanal en CSV",

                        data=csv_vista_semanal,

                        file_name=f"progreso_semanal_{datetime.now().strftime('%Y%m%d')}.csv",

                        mime="text/csv"

                    )

                else:

                    st.info("No hay datos semanales disponibles")



    # SubTab 4: Desempeño

    with subtab4:

        st.write("<h2 style='text-align: center;'>📈 Puntaje de Desempeño</h2>", unsafe_allow_html=True)

        df_desempeño.index = df_desempeño.index + 1
        st.dataframe(df_desempeño, width='stretch', height=400)

    

        csv_desempeño = df_desempeño.to_csv(index=False).encode('utf-8')

        st.download_button(

            label="📥 Descargar Desempeño en CSV",

            data=csv_desempeño,

            file_name=f"desempeño_datos_{datetime.now().strftime('%Y%m%d')}.csv",

            mime="text/csv"

        )



    # SubTab 5: Análisis por Métrica

    with subtab5:

        st.subheader("Análisis Detallado por Métrica")

    

        criterios_opciones = [

            'Presentaciòn',

            'Expresion Verbal / Diccion ',

            'Tiempo de Espera',

            'Validación de titular / contacto correcto',

            'Sondeo Asertivo ',

            'Identificación de necesidad',

            'Identificación de capacidad de pago / interés real',

            'Detección de decisor (titular o no)',

            'Escucha Activa',

            'Manejo de llamada',

            'Seguridad ',

            'Empatìa ',

            'Negocacion escalonada',

            'Beneficios claros',

            'Diferenciación vs competencia',

            'Personalización del discurso según necesidad',

            'Generación de urgencia',

            'Registro correcto en sistema ',

            'Uso adecuado de etiquetas'

        ]

    

        criterio_seleccionado = st.selectbox("Selecciona un criterio:", criterios_opciones)

    

        if criterio_seleccionado:

            # Buscar en la hoja Couching

            excel_file = encuentra_archivo_excel('CONTROL DE AUDITORIAS.xlsx')

            if excel_file is None:

                st.error("No se encontró el archivo CONTROL DE AUDITORIAS.xlsx")

            else:

                df_couching_raw = pd.read_excel(excel_file, sheet_name='Couching')

            

                # Buscar la columna exacta

                criterio_columna = None

                for col in df_couching_raw.columns:

                    if col.strip() == criterio_seleccionado.strip():

                        criterio_columna = col

                        break

            

                if criterio_columna:

                    puntos_maximos = {

                        'Presentaciòn': 1,

                        'Expresion Verbal / Diccion ': 4,

                        'Tiempo de Espera': 3,

                        'Validación de titular / contacto correcto': 2,

                        'Sondeo Asertivo ': 5,

                        'Identificación de necesidad': 7,

                        'Identificación de capacidad de pago / interés real': 4,

                        'Detección de decisor (titular o no)': 4,

                        'Escucha Activa': 7,

                        'Manejo de llamada': 12,

                        'Seguridad ': 5,

                        'Empatìa ': 8,

                        'Negocacion escalonada': 8,

                        'Beneficios claros': 8,

                        'Diferenciación vs competencia': 5,

                        'Personalización del discurso según necesidad': 7,

                        'Generación de urgencia': 5,

                        'Registro correcto en sistema ': 3,

                        'Uso adecuado de etiquetas': 2

                    }

                

                    puntaje_maximo = puntos_maximos.get(criterio_seleccionado, 'N/A')

            

                # Crear tabla de resultados

                resultados = []

                for idx, row in df_couching_raw.iterrows():

                    agente = str(row['Agentes Zimach']).strip()

                

                    if not agente or agente.lower() in ['total', 'sale conversion %', 'nan']:

                        continue

                

                    if 'ZIM_' not in agente.upper():

                        continue

                

                    try:

                        valor = row[criterio_columna]

                        if pd.isna(valor):

                            puntaje = '-'

                            porcentaje = '-'

                        else:

                            valor_str = str(valor).strip().upper()

                            if valor_str == 'N/A':

                                puntaje = '-'

                                porcentaje = '-'

                            else:

                                num_valor = float(valor)

                                puntaje = int(num_valor) if num_valor == int(num_valor) else round(num_valor, 2)

                            

                                if puntaje_maximo != 'N/A' and isinstance(puntaje_maximo, (int, float)):

                                    pct = (puntaje / puntaje_maximo) * 100

                                    porcentaje = f'{int(pct)}%' if pct == int(pct) else f'{pct:.2f}%'

                                else:

                                    porcentaje = '-'

                    except:

                        puntaje = '-'

                        porcentaje = '-'

                

                    resultados.append({

                        'Agentes Zimach': agente,

                        'Puntaje': puntaje,

                        'Porcentaje (%)': porcentaje

                    })

            

                if resultados:

                    df_resultado = pd.DataFrame(resultados)

                

                    # Información del criterio

                    col1, col2 = st.columns([2, 1])

                    with col1:

                        st.write(f"**Criterio:** {criterio_seleccionado}")

                    with col2:

                        st.write(f"**Puntaje Máximo:** {puntaje_maximo}")

                

                    # Convertir porcentajes a números para cálculos

                    def extraer_numero(val):

                        try:

                            return float(str(val).replace('%', ''))

                        except:

                            return 0

                

                    df_resultado['Pct_num'] = df_resultado['Porcentaje (%)'].apply(extraer_numero)

                    pct_promedio = df_resultado['Pct_num'].mean()

                

                    # Mostrar estadísticas

                    col_stats1, col_stats2, col_stats3 = st.columns(3)

                    with col_stats1:

                        st.metric("📊 Porcentaje Promedio", f"{pct_promedio:.1f}%")

                    with col_stats2:

                        pct_max = df_resultado['Pct_num'].max()

                        st.metric("⬆️ Máximo", f"{pct_max:.1f}%")

                    with col_stats3:

                        pct_min = df_resultado['Pct_num'].min()

                        pct_min = 0 if pct_min == 0 and all(df_resultado['Porcentaje (%)'] != '-') else pct_min

                        st.metric("⬇️ Mínimo", f"{pct_min:.1f}%")

                

                    st.write("")

                

                    # Crear tabla mejorada con colores y barras

                    html_resultado = """

                    <style>

                        .tabla-metricas { width: 100%; border-collapse: collapse; margin: 15px 0; }

                        .tabla-metricas thead { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; }

                        .tabla-metricas th { padding: 12px; text-align: left; font-weight: bold; }

                        .tabla-metricas td { padding: 12px; border-bottom: 1px solid #ddd; }

                        .tabla-metricas tbody tr:hover { background-color: #f5f5f5; }

                        .barra-progreso { height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden; }

                        .barra-contenido { height: 100%; border-radius: 4px; }

                        .excelente { background: linear-gradient(90deg, #28a745 0%, #20c997 100%); }

                        .bueno { background: linear-gradient(90deg, #17a2b8 0%, #20c997 100%); }

                        .aceptable { background: linear-gradient(90deg, #ffc107 0%, #fd7e14 100%); }

                        .bajo { background: linear-gradient(90deg, #dc3545 0%, #e74c3c 100%); }

                        .agente-col { font-weight: 500; color: #333; }

                        .puntaje-col { text-align: center; font-weight: bold; }

                        .porcentaje-col { text-align: center; font-weight: bold; }

                    </style>

                    <table class="tabla-metricas">

                        <thead>

                            <tr>

                                <th style="width: 40%;">🧑 Agente</th>

                                <th style="width: 15%; text-align: center;">Puntaje</th>

                                <th style="width: 45%;">Desempeño</th>

                            </tr>

                        </thead>

                        <tbody>

                    """

                

                    for idx, row in df_resultado.iterrows():

                        agente = row['Agentes Zimach']

                        puntaje = row['Puntaje']

                        porcentaje_str = row['Porcentaje (%)']

                        pct_num = row['Pct_num']

                    

                        # Determinar clase de color según desempeño

                        if pct_num >= 80:

                            clase_barra = 'excelente'

                            nivel = '⭐ Excelente'

                        elif pct_num >= 60:

                            clase_barra = 'bueno'

                            nivel = '👍 Bueno'

                        elif pct_num >= 40:

                            clase_barra = 'aceptable'

                            nivel = '⚠️ Aceptable'

                        else:

                            clase_barra = 'bajo'

                            nivel = '❌ Por Mejorar'

                    

                        html_resultado += '<tr><td class="agente-col">' + str(agente) + '</td><td class="puntaje-col">' + str(puntaje) + '/' + str(puntaje_maximo) + '</td><td><div style="margin-bottom: 5px;"><div class="barra-progreso"><div class="barra-contenido ' + clase_barra + '" style="width: ' + str(pct_num) + '%;"></div></div><small style="color: #666;">' + porcentaje_str + ' - ' + nivel + '</small></div></td></tr>'

                

                    html_resultado += '</tbody></table>'

                

                    st.markdown(html_resultado, unsafe_allow_html=True)

                

                    csv_criterio = df_resultado[['Agentes Zimach', 'Puntaje', 'Porcentaje (%)']].to_csv(index=False).encode('utf-8')

                    st.download_button(

                        label="📥 Descargar en CSV",

                        data=csv_criterio,

                        file_name=f"{criterio_seleccionado}_{datetime.now().strftime('%Y%m%d')}.csv",

                        mime="text/csv"

                    )



    # SubTab 6: Leyenda de Métricas

    with subtab6:

        st.subheader("Leyenda de Métricas - Criterios y Puntajes")

        st.info("Esta tabla muestra todos los criterios de evaluación, sus descripciones, puntajes máximos y la categoría a la que pertenecen.")

        df_metricas.index = df_metricas.index + 1
        st.dataframe(df_metricas, width='stretch', height=600)

    

        csv_metricas = df_metricas.to_csv(index=False).encode('utf-8')

        st.download_button(

            label="📥 Descargar Métricas en CSV",

            data=csv_metricas,

            file_name=f"metricas_{datetime.now().strftime('%Y%m%d')}.csv",

            mime="text/csv"

        )



    # SubTab 7: Niveles de Intensidad Sugeridos

    with subtab7:

        st.write("<h2 style='text-align: center;'>🎯 Niveles de Intensidad Sugeridos</h2>", unsafe_allow_html=True)

    

        # Crear columnas para los tres niveles

        col_baja, col_media, col_alta = st.columns(3)

    

        # Nivel Baja

        with col_baja:

            st.markdown("""

            <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 25px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; height: 100%; min-height: 400px;">

                <h3 style="margin-top: 0; font-size: 1.8rem;">Baja</h3>

                <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">

                <div style="text-align: left; line-height: 1.8;">

                    <p><strong>📌 Feedback Semanal</strong></p>

                    <p style="margin-top: 15px;">• 1 feedback semanal</p>

                    <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">

                    <p><strong>🎧 Escucha Guiada</strong></p>

                    <p style="margin-top: 15px;">• 1 escucha guiada</p>

                    <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">

                    <p><strong>🎭 Roleplay</strong></p>

                    <p style="margin-top: 15px;">• Sin roleplay</p>

                </div>

            </div>

            """, unsafe_allow_html=True)

    

        # Nivel Media

        with col_media:

            st.markdown("""

            <div style="background: linear-gradient(135deg, #fd7e14 0%, #ffc107 100%); padding: 25px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; height: 100%; min-height: 400px;">

                <h3 style="margin-top: 0; font-size: 1.8rem;">Media</h3>

                <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">

                <div style="text-align: left; line-height: 1.8;">

                    <p><strong>📌 Feedback Semanal</strong></p>

                    <p style="margin-top: 15px;">• 2 feedbacks semanales</p>

                    <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">

                    <p><strong>🎧 Escucha Guiada</strong></p>

                    <p style="margin-top: 15px;">• 2 escuchas + checklist</p>

                    <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">

                    <p><strong>🎭 Roleplay</strong></p>

                    <p style="margin-top: 15px;">• 1 roleplay</p>

                </div>

            </div>

            """, unsafe_allow_html=True)

    

        # Nivel Alta

        with col_alta:

            st.markdown("""

            <div style="background: linear-gradient(135deg, #dc3545 0%, #e74c3c 100%); padding: 25px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; height: 100%; min-height: 400px;">

                <h3 style="margin-top: 0; font-size: 1.8rem;">Alta</h3>

                <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">

                <div style="text-align: left; line-height: 1.8;">

                    <p><strong>📌 Feedback Diario</strong></p>

                    <p style="margin-top: 15px;">• Feedback diario</p>

                    <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">

                    <p><strong>🎧 Escucha en Vivo</strong></p>

                    <p style="margin-top: 15px;">• Escucha + corrección en vivo</p>

                    <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">

                    <p><strong>🎭 Roleplay Constante</strong></p>

                    <p style="margin-top: 15px;">• Roleplay constante

                    <p style="margin-top: 8px;">• Seguimiento de speech</p>

                </div>

            </div>

            """, unsafe_allow_html=True)



    # ==============================================
    # TAB CONTROL DE CALIDAD
    # ==============================================

with tab_control_calidad:

    st.write("<h2 style='text-align: center;'>📊 Control de Calidad</h2>", unsafe_allow_html=True)
    
    # Calcular indicadores de Control de Calidad
    if not df_control_calidad.empty:
        total_leads = df_control_calidad['Leads'].sum()
        
        # Calcular totales de Sin Calificar y Exactitud
        total_sin_calificar_q = df_control_calidad['Sin Calificar Q'].sum()
        total_exactitud_q = df_control_calidad['Exactitud Q'].sum()
        total_barrido_q = total_sin_calificar_q + total_exactitud_q
        
        # Calcular porcentajes sobre el total de leads
        prom_sin_calificar = (total_sin_calificar_q / total_leads * 100) if total_leads > 0 else 0
        prom_exactitud = (total_exactitud_q / total_leads * 100) if total_leads > 0 else 0
        barrido_pct = (total_barrido_q / total_leads * 100) if total_leads > 0 else 0
        
        # Mostrar indicadores principales
        st.markdown("### 📊 Indicadores Principales de Calidad")
        
        # Primera fila de indicadores
        col1_cc, col2_cc = st.columns(2)
        
        with col1_cc:
            st.write(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">📋 Total Leads</div>
                    <div style="font-size: 2.5rem; font-weight: bold; margin: 10px 0;">{int(total_leads)}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2_cc:
            st.write(f"""
                <div style="background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">🎯 TOTAL DE DESVIOS</div>
                    <div style="font-size: 2.5rem; font-weight: bold; margin: 10px 0;">{barrido_pct:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Segunda fila de indicadores
        col3_cc, col4_cc = st.columns(2)
        
        with col3_cc:
            st.write(f"""
                <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ffa94d 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">⚠️ Total Sin Calificar</div>
                    <div style="font-size: 2.5rem; font-weight: bold; margin: 10px 0;">{prom_sin_calificar:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4_cc:
            st.write(f"""
                <div style="background: linear-gradient(135deg, #28a745 0%, #51cf66 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">✅ Total Exactitud</div>
                    <div style="font-size: 2.5rem; font-weight: bold; margin: 10px 0;">{prom_exactitud:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### �📋 Detalles por Agente")

        # Crear tabla HTML personalizada con estilo mejorado
        html_tabla = """
        <style>
            .tabla-calidad {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 13px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                overflow: hidden;
                background-color: white;
            }
            .tabla-calidad thead {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .tabla-calidad th {
                padding: 14px 10px;
                text-align: center;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            .tabla-calidad tbody tr {
                border-bottom: 1px solid #e9ecef;
            }
            .tabla-calidad tbody tr:hover {
                background-color: #f8f9ff;
            }
            .tabla-calidad tbody tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            .tabla-calidad td {
                padding: 12px 10px;
                text-align: center;
            }
            .agente-col {
                text-align: left;
                font-weight: 500;
                color: #333;
            }
            .leads-col {
                font-weight: bold;
                color: #667eea;
            }
            .notificado-alto { color: #dc3545; font-weight: bold; }
            .notificado-medio { color: #fd7e14; font-weight: bold; }
            .notificado-bajo { color: #28a745; font-weight: bold; }
            .exactitud-bajo { color: #dc3545; font-weight: bold; }
            .exactitud-medio { color: #fd7e14; font-weight: bold; }
            .exactitud-alto { color: #28a745; font-weight: bold; }
            .cobertura-col { color: #1e90ff; font-weight: bold; }
            .no-evaluado-col { color: #6c757d; font-weight: bold; }
            .desvio-alto { color: #dc3545; font-weight: bold; }
            .desvio-medio { color: #fd7e14; font-weight: bold; }
            .desvio-bajo { color: #28a745; font-weight: bold; }
        </style>
        <table class="tabla-calidad">
            <thead>
                <tr>
                    <th>Agente</th>
                    <th>Leads</th>
                    <th>Sin Cal. Q</th>
                    <th>Sin Cal. %</th>
                    <th>Exactitud Q</th>
                    <th>Exactitud %</th>
                    <th>Validación de Cobertura %</th>
                    <th>No Evaluado %</th>
                    <th>% Total de Desvios</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Preparar datos para ordenar por Total de Desvios
        df_tabla = df_control_calidad.copy()
        df_tabla = df_tabla.merge(df_validacion_cobertura[['Agente', 'Validacion Cobertura %', 'No Evaluado %']], on='Agente', how='left')
        df_tabla['Validacion Cobertura %'] = df_tabla['Validacion Cobertura %'].fillna(0)
        df_tabla['No Evaluado %'] = df_tabla['No Evaluado %'].fillna(0)
        
        # Calcular Total de Desvios (casos tipificados / total leads * 100)
        # Recargar datos del Excel para hacer el cálculo correcto
        try:
            excel_file = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')
            if excel_file:
                df_raw = pd.read_excel(excel_file, sheet_name=0)
                df_raw = df_raw[df_raw['AGENTE'] != 'Sin agente'].copy()
                df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'], format='%d/%m/%Y', errors='coerce')
                df_raw['Mes'] = df_raw['Fecha'].dt.month
                df_raw['Año'] = df_raw['Fecha'].dt.year
                df_raw = df_raw[(df_raw['Mes'] == mes_numero_filtro) & (df_raw['Año'] == año_filtro)].copy()
                
                # Filtrar usuarios ficticios
                usuarios_ficticios = ['ZIM_FLAVIOZM_VTP', 'ZIM_KATHERINEMM_VTP', 'ZIM_CARLOSVG_VTP', 'ZIM_ANTHONYJR_VTP']
                df_raw = df_raw[~df_raw['AGENTE'].isin(usuarios_ficticios)].copy()
                
                # Calcular casos tipificados por agente (todos excepto nulls)
                casos_tipificados = df_raw[df_raw['STATUS'].notna()].groupby('AGENTE').size().reset_index(name='Tipificados')
                total_por_agente = df_raw['AGENTE'].value_counts().reset_index()
                total_por_agente.columns = ['AGENTE', 'Total']
                
                desvios_data = casos_tipificados.merge(total_por_agente, left_on='AGENTE', right_on='AGENTE', how='left')
                desvios_data.columns = ['Agente', 'Tipificados', 'Total']
                desvios_data['Total Desvios'] = (desvios_data['Tipificados'] / desvios_data['Total'] * 100).round(2)
                
                # Merge con df_tabla
                df_tabla = df_tabla.merge(desvios_data[['Agente', 'Total Desvios']], on='Agente', how='left')
            else:
                # Si no se puede recargar, usar suma de porcentajes como fallback
                df_tabla['Total Desvios'] = df_tabla.apply(
                    lambda row: (
                        float(str(row['Sin Calificar %']).rstrip('%').strip() or 0) +
                        float(str(row['Exactitud %']).rstrip('%').strip() or 0) +
                        float(row['Validacion Cobertura %'])
                    ),
                    axis=1
                )
        except:
            # Fallback: usar suma de porcentajes
            df_tabla['Total Desvios'] = df_tabla.apply(
                lambda row: (
                    float(str(row['Sin Calificar %']).rstrip('%').strip() or 0) +
                    float(str(row['Exactitud %']).rstrip('%').strip() or 0) +
                    float(row['Validacion Cobertura %'])
                ),
                axis=1
            )
        
        # Ordenar por Total de Desvios descendente (mayor a menor)
        df_tabla['Total Desvios'] = pd.to_numeric(df_tabla['Total Desvios'], errors='coerce')
        df_tabla = df_tabla.sort_values('Total Desvios', ascending=False, na_position='last').reset_index(drop=True)
        
        for idx, row in df_tabla.iterrows():
            agente = str(row['Agente']).strip()
            leads = int(row['Leads'])
            sin_q = int(row['Sin Calificar Q'])
            sin_pct_str = str(row['Sin Calificar %']).rstrip('%').strip()
            exact_q = int(row['Exactitud Q'])
            exact_pct_str = str(row['Exactitud %']).rstrip('%').strip()
            
            # Obtener Validación de Cobertura y No Evaluado de la fila actual
            validacion_cobertura_pct = float(row['Validacion Cobertura %'])
            no_evaluado_pct = float(row['No Evaluado %'])
            
            try:
                sin_pct = float(sin_pct_str)
                exact_pct = float(exact_pct_str)
            except:
                sin_pct = 0
                exact_pct = 0
            
            # Determinar clase para Sin Calificar
            if sin_pct > 10:
                sin_clase = "notificado-alto"
            elif sin_pct > 5:
                sin_clase = "notificado-medio"
            else:
                sin_clase = "notificado-bajo"
            
            # Determinar clase para Exactitud
            if exact_pct >= 90:
                exact_clase = "exactitud-alto"
            elif exact_pct >= 80:
                exact_clase = "exactitud-medio"
            else:
                exact_clase = "exactitud-bajo"
            
            # Calcular Total de Desvios
            total_desvios = sin_pct + exact_pct + validacion_cobertura_pct
            
            # Determinar clase para Total de Desvios
            if total_desvios > 5:
                desvio_clase = "desvio-alto"
            elif total_desvios >= 1:
                desvio_clase = "desvio-medio"
            else:
                desvio_clase = "desvio-bajo"
            
            html_tabla += f'<tr><td class="agente-col">{agente}</td><td class="leads-col">{leads}</td><td>{sin_q}</td><td class="{sin_clase}">{sin_pct_str}%</td><td>{exact_q}</td><td class="{exact_clase}">{exact_pct_str}%</td><td class="cobertura-col">{validacion_cobertura_pct:.2f}%</td><td class="no-evaluado-col">{no_evaluado_pct:.2f}%</td><td class="{desvio_clase}">{total_desvios:.2f}%</td></tr>'
        
        html_tabla += '</tbody></table>'
        
        st.markdown(html_tabla, unsafe_allow_html=True)
        
        # Tabla de Semanas
        st.markdown("---")
        st.markdown("### 📅 Comportamiento por Semana (Sin Calificar vs Exactitud)")
        
        # Filtros
        col_filtro1, col_filtro2 = st.columns([1, 2])
        
        with col_filtro1:
            tipo_filtro = st.radio(
                "Mostrar:",
                options=["Ambos", "Solo Sin Calificar", "Solo Exactitud"],
                horizontal=False,
                key="filtro_semanas"
            )
        
        with col_filtro2:
            agentes_lista = ["Todos"] + sorted(df_semanas['Agente'].unique().tolist())
            agente_seleccionado = st.selectbox(
                "Seleccionar Agente:",
                options=agentes_lista,
                key="filtro_agente_semanas"
            )
        
        if not df_semanas.empty:
            # Filtrar por agente si es necesario
            if agente_seleccionado == "Todos":
                df_mostrar_semanas = df_semanas.copy()
            else:
                df_mostrar_semanas = df_semanas[df_semanas['Agente'] == agente_seleccionado].copy()
            
            if df_mostrar_semanas.empty:
                if agente_seleccionado == "Todos":
                    st.info("No hay datos disponibles de semanas.")
                else:
                    st.info(f"No hay datos para el agente: {agente_seleccionado}")
            else:
                # Preparar datos para el gráfico
                semanas = ['S1', 'S2', 'S3', 'S4', 'S5']
                
                import plotly.graph_objects as go
                fig = go.Figure()
                
                # Colores para las líneas
                color_sin = '#dc3545'  # Rojo
                color_exactitud = '#28a745'  # Verde
                
                # Calcular sumas totales por semana
                total_sin = [0] * 5
                total_exactitud = [0] * 5
                
                for idx, row in df_mostrar_semanas.iterrows():
                    # Valores de Sin Calificar
                    for i in range(5):
                        sin_val = int(row[f'Sin_S{i+1}']) if pd.notna(row[f'Sin_S{i+1}']) else 0
                        total_sin[i] += sin_val
                        
                    # Valores de Exactitud
                    for i in range(5):
                        exact_val = int(row[f'Exactitud_S{i+1}']) if pd.notna(row[f'Exactitud_S{i+1}']) else 0
                        total_exactitud[i] += exact_val
                
                # Agregar líneas según el filtro
                if tipo_filtro in ["Ambos", "Solo Sin Calificar"]:
                    fig.add_trace(go.Scatter(
                        x=semanas,
                        y=total_sin,
                        mode='lines+markers',
                        name='Total Sin Calificar',
                        line=dict(color=color_sin, width=3),
                        marker=dict(size=10)
                    ))
                
                if tipo_filtro in ["Ambos", "Solo Exactitud"]:
                    fig.add_trace(go.Scatter(
                        x=semanas,
                        y=total_exactitud,
                        mode='lines+markers',
                        name='Total Exactitud',
                        line=dict(color=color_exactitud, width=3),
                        marker=dict(size=10)
                    ))
                
                # Actualizar layout
                fig.update_layout(
                    title="Tendencia de Calificación por Semana",
                    xaxis_title="Semana",
                    yaxis_title="Cantidad",
                    height=500,
                    hovermode='x unified',
                    template='plotly_white',
                    font=dict(size=12),
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01,
                        bgcolor="rgba(255, 255, 255, 0.8)"
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Gráfico de barras - % Total de Desvios por Agente
                st.markdown("---")
                st.markdown("### 📊 % Total de Desvios por Agente (Casos Tipificados)")
                
                # Calcular % Total de Desvios (casos tipificados / total leads) filtrado por mes
                if mes_filtro_global and mes_numero_filtro and año_filtro:
                    try:
                        excel_file = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')
                        if excel_file:
                            df_raw = pd.read_excel(excel_file, sheet_name=0)
                            df_raw = df_raw[df_raw['AGENTE'] != 'Sin agente'].copy()
                            df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'], format='%d/%m/%Y', errors='coerce')
                            df_raw['Mes'] = df_raw['Fecha'].dt.month
                            df_raw['Año'] = df_raw['Fecha'].dt.year
                            df_raw = df_raw[(df_raw['Mes'] == mes_numero_filtro) & (df_raw['Año'] == año_filtro)].copy()
                            
                            # Contar total de leads por agente
                            total_por_agente = df_raw['AGENTE'].value_counts().reset_index()
                            total_por_agente.columns = ['Agente', 'Total']
                            
                            # Contar CASOS TIPIFICADOS (STATUS no es nulo)
                            df_tipificados = df_raw[df_raw['STATUS'].notna()]
                            tipificados_por_agente = df_tipificados['AGENTE'].value_counts().reset_index()
                            tipificados_por_agente.columns = ['Agente', 'Tipificados']
                            
                            # Combinar datos
                            resultado = total_por_agente.copy()
                            resultado = resultado.merge(tipificados_por_agente, on='Agente', how='left')
                            resultado['Tipificados'] = resultado['Tipificados'].fillna(0).astype(int)
                            resultado['% Desvios'] = (resultado['Tipificados'] / resultado['Total'] * 100).round(2)
                            resultado = resultado.sort_values('% Desvios', ascending=False).reset_index(drop=True)
                            
                            df_barras = resultado
                        else:
                            df_barras = pd.DataFrame()
                    except Exception as e:
                        df_barras = pd.DataFrame()
                else:
                    df_barras = pd.DataFrame()
                
                if not df_barras.empty:
                    import plotly.graph_objects as go
                    
                    # Definir colores según el porcentaje
                    colores = []
                    for val in df_barras['% Desvios']:
                        if val >= 95:
                            colores.append('#28a745')  # Verde - Excelente
                        elif val >= 85:
                            colores.append('#fd7e14')  # Naranja - Moderado
                        else:
                            colores.append('#dc3545')  # Rojo - Bajo
                    
                    fig_barras = go.Figure(data=[
                        go.Bar(
                            x=df_barras['Agente'],
                            y=df_barras['% Desvios'],
                            marker=dict(color=colores),
                            text=df_barras['% Desvios'].round(2),
                            textposition='outside',
                            hovertemplate='<b>%{x}</b><br>Casos Tipificados: %{customdata[0]}<br>Total Leads: %{customdata[1]}<br>% Desvios: %{y:.2f}%<extra></extra>',
                            customdata=df_barras[['Tipificados', 'Total']].values
                        )
                    ])
                    
                    fig_barras.update_layout(
                        title="% Total de Desvios por Agente (Casos Tipificados / Total Leads)",
                        xaxis_title="Agente",
                        yaxis_title="Porcentaje (%)",
                        height=500,
                        template='plotly_white',
                        showlegend=False,
                        font=dict(size=11),
                        xaxis=dict(tickangle=-45),
                        yaxis=dict(range=[0, 105])
                    )
                    
                    st.plotly_chart(fig_barras, use_container_width=True)

    else:

        st.warning("No hay datos disponibles en el archivo de Control de Calidad.")

    # ========================================
    # NUEVA SECCIÓN: KPIs EXAMEN BITEL
    # ========================================
    
    st.markdown("---")
    st.markdown("## 🎓 KPIs de Examen de Calidad BITEL")
    
    if not df_examen_bitel.empty:
        # Calcular KPIs
        kpis_general = calcular_kpis_rendimiento_general(df_examen_bitel)
        kpis_asesor = calcular_kpis_por_asesor(df_examen_bitel)
        kpis_temporal = calcular_kpis_temporales(df_examen_bitel)
        
        # SECCIÓN 1: Indicadores de Rendimiento General
        st.markdown("### 📊 Indicadores de Rendimiento General")
        
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        
        with col_kpi1:
            st.write(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">🎯 Puntaje Promedio</div>
                    <div style="font-size: 2.2rem; font-weight: bold; margin: 10px 0;">{kpis_general.get('promedio_global', 0):.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_kpi2:
            st.write(f"""
                <div style="background: linear-gradient(135deg, #28a745 0%, #51cf66 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">✅ % Aprobación</div>
                    <div style="font-size: 2.2rem; font-weight: bold; margin: 10px 0;">{kpis_general.get('pct_aprobacion', 0):.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_kpi3:
            st.write(f"""
                <div style="background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">📋 Total Evaluaciones</div>
                    <div style="font-size: 2.2rem; font-weight: bold; margin: 10px 0;">{kpis_general.get('total_evaluaciones', 0)}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_kpi4:
            # Calcular el porcentaje de evaluaciones en nivel bajo sobre total de asesores
            total_asesores_para_kpi = len(kpis_asesor) if not kpis_asesor.empty else 1
            asesores_bajo_para_kpi = len(kpis_asesor[kpis_asesor['Tiene Bajo'] == 'Sí']) if not kpis_asesor.empty else 0
            pct_asesores_bajo = (asesores_bajo_para_kpi / total_asesores_para_kpi * 100) if total_asesores_para_kpi > 0 else 0
            
            st.write(f"""
                <div style="background: linear-gradient(135deg, #dc3545 0%, #e74c3c 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">⚠️ % Asesores Nivel Bajo</div>
                    <div style="font-size: 2.2rem; font-weight: bold; margin: 10px 0;">{pct_asesores_bajo:.2f}%</div>
                    <div style="font-size: 0.85rem; opacity: 0.9;">({asesores_bajo_para_kpi} de {total_asesores_para_kpi})</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # SECCIÓN 2: Gráficos de Distribución
        col_grafico1, col_grafico2 = st.columns(2)
        
        with col_grafico1:
            # Gráfico de pastel: Distribución por Nivel
            dist_nivel = kpis_general.get('distribucion_nivel', {})
            if dist_nivel:
                fig_nivel = go.Figure(data=[go.Pie(
                    labels=list(dist_nivel.keys()),
                    values=list(dist_nivel.values()),
                    marker=dict(colors=['#dc3545', '#fd7e14', '#28a745']),
                    textposition='inside',
                    textinfo='label+percent'
                )])
                fig_nivel.update_layout(
                    title="Distribución de Evaluaciones por Nivel",
                    height=400
                )
                st.plotly_chart(fig_nivel, use_container_width=True)
        
        with col_grafico2:
            # Gráfico de barras: Promedio por Tipo de Examen
            promedio_por_tipo = kpis_general.get('promedio_por_tipo', {})
            if promedio_por_tipo:
                fig_tipo = go.Figure(data=[go.Bar(
                    x=list(promedio_por_tipo.keys()),
                    y=list(promedio_por_tipo.values()),
                    marker=dict(color='#667eea'),
                    text=[f"{v:.2f}" for v in promedio_por_tipo.values()],
                    textposition='outside'
                )])
                fig_tipo.update_layout(
                    title="Promedio de Puntaje por Tipo de Examen",
                    xaxis_title="Tipo de Examen",
                    yaxis_title="Puntaje Promedio",
                    height=400,
                    xaxis=dict(tickangle=-45)
                )
                st.plotly_chart(fig_tipo, use_container_width=True)
        
        st.markdown("---")
        
        # SECCIÓN 3: Indicadores por Asesor
        st.markdown("### 👤 Indicadores por Asesor")
        
        if not kpis_asesor.empty:
            # Estadísticas de asesores
            total_asesores_unicos = len(kpis_asesor)
            col_asesor1, col_asesor2, col_asesor3 = st.columns(3)
            
            with col_asesor1:
                asesores_con_bajo = len(kpis_asesor[kpis_asesor['Tiene Bajo'] == 'Sí'])
                pct_asesores_con_bajo = (asesores_con_bajo / total_asesores_unicos * 100) if total_asesores_unicos > 0 else 0
                st.write(f"""
                    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ffa94d 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">👥 % Asesores con Nivel Bajo</div>
                        <div style="font-size: 2.2rem; font-weight: bold; margin: 10px 0;">{pct_asesores_con_bajo:.2f}%</div>
                        <div style="font-size: 0.85rem; opacity: 0.9;">({asesores_con_bajo} de {total_asesores_unicos})</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_asesor2:
                st.write(f"""
                    <div style="background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">👥 Total Asesores Únicos</div>
                        <div style="font-size: 2.2rem; font-weight: bold; margin: 10px 0;">{total_asesores_unicos}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_asesor3:
                promedio_aprobacion = kpis_asesor['% Aprobación'].mean()
                st.write(f"""
                    <div style="background: linear-gradient(135deg, #51cf66 0%, #28a745 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">🎯 % Aprobación Promedio</div>
                        <div style="font-size: 2rem; font-weight: bold; margin: 10px 0;">{promedio_aprobacion:.2f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Tabla de asesores
            st.markdown("#### 📋 Desempeño Detallado por Asesor")
            
            # Ordenar por Evals Nivel Bajo descendente
            kpis_asesor_sorted = kpis_asesor.sort_values('Evals Nivel Bajo', ascending=False).reset_index(drop=True)
            
            # Mostrar tabla con dataframe de Streamlit
            st.dataframe(kpis_asesor_sorted, use_container_width=True, hide_index=True)
            
            # Descarga de datos
            csv_asesor = kpis_asesor_sorted.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Desempeño por Asesor en CSV",
                data=csv_asesor,
                file_name=f"kpi_asesor_examen_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        st.markdown("---")
        
        # SECCIÓN 4: Indicadores Temporales
        st.markdown("### 📅 Indicadores Temporales")
        
        kpis_temporal_data = kpis_temporal
        col_temp1, col_temp2 = st.columns(2)
        
        with col_temp1:
            st.write(f"""
                <div style="background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">📋 Volumen Total de Evaluaciones</div>
                    <div style="font-size: 2rem; font-weight: bold; margin: 10px 0;">{kpis_temporal_data.get('total_evaluaciones', 0)}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_temp2:
            st.write(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">📊 Promedio Evals/Semana</div>
                    <div style="font-size: 2rem; font-weight: bold; margin: 10px 0;">{kpis_temporal_data.get('promedio_evals_semana', 0):.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de evaluaciones por semana
        evals_por_semana = kpis_temporal_data.get('evals_por_semana', {})
        if evals_por_semana:
            st.markdown("---")
            st.markdown("#### 📈 Volumen de Evaluaciones por Semana (Marzo - Abril 2026)")
            
            semanas = list(evals_por_semana.keys())
            valores = list(evals_por_semana.values())
            
            fig_temporal = go.Figure(data=[go.Bar(
                x=semanas,
                y=valores,
                marker=dict(color='#51cf66'),
                text=valores,
                textposition='outside'
            )])
            fig_temporal.update_layout(
                title="Evaluaciones Realizadas por Semana",
                xaxis_title="Semana (YYYY-WXX)",
                yaxis_title="Cantidad de Evaluaciones",
                height=400,
                template='plotly_white',
                xaxis=dict(tickangle=-45)
            )
            st.plotly_chart(fig_temporal, use_container_width=True)
    
    else:
        st.warning("⚠️ No hay datos disponibles en el archivo **CONSOLIDADO EXAMEN BITEL.xlsx**")



# Footer

st.markdown("---")

st.markdown("""

    <div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 20px;">

        <p>📊 Dashboard de Control de Auditorías | Actualizado: """ + datetime.now().strftime('%d/%m/%Y %H:%M') + """</p>

    </div>

""", unsafe_allow_html=True)
