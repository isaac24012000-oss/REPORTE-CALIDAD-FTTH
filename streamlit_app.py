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
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
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
                return '🟢 Mejora significativa'
            elif 1 <= row['Δ vs anterior'] < 5:
                return '🟡 Mejora leve'
            elif row['Δ vs anterior'] == 0:
                return '⚪ Estabilidad'
            else:
                return '🔴 Decremento'
        
        df['Progreso'] = df.apply(obtener_progreso, axis=1)
        
        # Formatear Δ vs anterior para mostrar
        df['Δ vs anterior_str'] = df['Δ vs anterior'].apply(
            lambda x: '-' if pd.isna(x) else (f'{x:+.1f}%' if x != 0 else '0%')
        )
        
        # Formatear Calidad (%) a porcentaje
        df['Calidad (%)_str'] = df['Calidad (%)'].apply(lambda x: f'{x:.1f}%' if pd.notna(x) else '-')
        
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
                    return '⭐ Primera evaluación'
                elif delta >= 5:
                    return '🟢 Mejora significativa'
                elif 1 <= delta < 5:
                    return '🟡 Mejora leve'
                elif -1 < delta < 1 and delta != 0:
                    return '⚪ Estable (cambio mínimo)'
                elif delta == 0:
                    return '⚪ Estable'
                else:
                    return '🔴 Decremento'
            
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
                estado = '🟢 Mejora significativa'
            elif 1 <= delta_promedio < 5:
                estado = '🟡 Mejora leve'
            elif -1 < delta_promedio <= 0:
                estado = '⚪ Estable'
            else:
                estado = '🔴 Decremento'
            
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
def cargar_datos_control_calidad():
    """Carga los datos de Control de Calidad del archivo REPORTE CALIDAD.xlsx"""
    try:
        excel_file = encuentra_archivo_excel('REPORTE CALIDAD.xlsx')
        
        if excel_file is None:
            st.error("No se encontró el archivo REPORTE CALIDAD.xlsx")
            return pd.DataFrame()
        
        df = pd.read_excel(excel_file, sheet_name=0)
        
        # Contar leads por agente
        leads_por_agente = df['AGENTE'].value_counts().reset_index()
        leads_por_agente.columns = ['Agente', 'Leads']
        
        # Contar notificados (no SIN CALIFICAR)
        df_notificado = df[df['STATUS'].notna() & (df['STATUS'] != 'SIN CALIFICAR')]
        notificado_por_agente = df_notificado['AGENTE'].value_counts().reset_index()
        notificado_por_agente.columns = ['Agente', 'Notificado Q']
        
        # Contar exactitud (EXACTITUD o CORRECTO)
        df_exactitud = df[
            ((df['STATUS'] == 'CORRECTO') | (df['STATUSS'] == 'EXACTITUD'))
        ]
        exactitud_por_agente = df_exactitud['AGENTE'].value_counts().reset_index()
        exactitud_por_agente.columns = ['Agente', 'Exactitud Q']
        
        # Combinar todos los datos
        resultado = leads_por_agente.copy()
        resultado = resultado.merge(notificado_por_agente, on='Agente', how='left')
        resultado = resultado.merge(exactitud_por_agente, on='Agente', how='left')
        
        # Llenar NaN con 0
        resultado = resultado.fillna(0)
        
        # Convertir a enteros
        resultado['Notificado Q'] = resultado['Notificado Q'].astype(int)
        resultado['Exactitud Q'] = resultado['Exactitud Q'].astype(int)
        
        # Calcular porcentajes
        resultado['Notificado %'] = (resultado['Notificado Q'] / resultado['Leads'] * 100).round(2).astype(str) + '%'
        resultado['Exactitud %'] = (resultado['Exactitud Q'] / resultado['Leads'] * 100).round(2).astype(str) + '%'
        
        # Reordenar columnas
        resultado = resultado[['Agente', 'Leads', 'Notificado Q', 'Notificado %', 'Exactitud Q', 'Exactitud %']]
        
        # Ordenar por Agente
        resultado = resultado.sort_values('Agente').reset_index(drop=True)
        
        return resultado
    except Exception as e:
        st.error(f"Error al cargar datos de Control de Calidad: {str(e)}")
        return pd.DataFrame()

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

# Cálculos para estadísticas
excel_file = encuentra_archivo_excel('CONTROL DE AUDITORIAS.xlsx')
if excel_file:
    df_raw = pd.read_excel(excel_file, sheet_name='Data')
    df_raw_filtrado = df_raw[df_raw['Agentes Zimach'].astype(str).str.contains('ZIM_', case=False, na=False)]

    total_agentes = len(df_data)
    conv_promedio = df_raw_filtrado['Sale Conv %'].mean() * 100
    calidad_promedio = df_raw_filtrado['% calidad'].mean() * 100
else:
    total_agentes = 0
    conv_promedio = 0
    calidad_promedio = 0

# Header
st.markdown("## 📊 Dashboard - Control de Auditorías")
st.markdown("*Análisis de desempeño de agentes y métricas de calidad*")

# Métricas principales
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">👥 Total de Agentes</div>
            <div class="metric-value">{total_agentes}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">↔️ Conversión Promedio</div>
            <div class="metric-value">{conv_promedio:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⭐ Calidad Promedio</div>
            <div class="metric-value">{calidad_promedio:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

# Tabs para diferentes vistas
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    ["📋 Control de Auditorias", "📋 Plan de Acción", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad", "📊 Progreso de Plan", "📊 Control de Calidad"]
)

# Tab 1: Datos de Control
with tab1:
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
    
    # Aplicar colores al DataFrame
    df_coloreado = aplicar_colores_df(df_control_mejorado)
    
    # Convertir a HTML con colores
    html_tabla = df_coloreado.to_html(escape=False, index=False)
    html_tabla = f"""
    <div style="display: flex; justify-content: center; width: 100%;">
        <div style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px;">
            {html_tabla}
        </div>
    </div>
    """
    st.markdown(html_tabla, unsafe_allow_html=True)
    
    # Descargar datos
    csv_data = df_control_mejorado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Control en CSV",
        data=csv_data,
        file_name=f"control_datos_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Tab 2: Plan de Acción
with tab2:
    st.write("<h2 style='text-align: center;'>📋 Plan de Acción</h2>", unsafe_allow_html=True)
    st.dataframe(df_couching, width='stretch', height=400)
    
    csv_couching = df_couching.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Plan de Acción en CSV",
        data=csv_couching,
        file_name=f"plan_accion_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Tab 3: Progreso de Plan
with tab3:
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
                                    icono = "🟢"
                                    titulo = "Mejora Significativa"
                                    recomendacion = f"¡Excelente! {agente} está demostrando un incremento sostenido de <strong>+{delta_promedio:.2f}%</strong> en su desempeño. Continúa con las estrategias actuales de coaching. Se recomienda evaluar qué está funcionando bien y replicarlo en otras áreas."
                                elif 1 <= delta_promedio < 5:
                                    color_bg = "#fff3cd"
                                    color_border = "#ffc107"
                                    icono = "🟡"
                                    titulo = "Mejora Leve"
                                    recomendacion = f"{agente} está avanzando con una mejora leve de <strong>+{delta_promedio:.2f}%</strong>. Se recomienda intensificar el coaching enfocándose en las áreas críticas. Realiza feedback más frecuentes y establece objetivos más claros."
                                elif -1 < delta_promedio <= 0:
                                    color_bg = "#f8f9fa"
                                    color_border = "#6c757d"
                                    icono = "⚪"
                                    titulo = "Estable"
                                    recomendacion = f"{agente} está manteniendo su nivel con cambios mínimos de <strong>{delta_promedio:.2f}%</strong>. Analiza si necesita más apoyo o nuevas estrategias de coaching para generar impulso."
                                else:
                                    color_bg = "#f8d7da"
                                    color_border = "#dc3545"
                                    icono = "🔴"
                                    titulo = "Sin Mejora"
                                    recomendacion = f"{agente} presenta un decremento de <strong>{delta_promedio:.2f}%</strong>. Se requiere intervención inmediata. Realiza una evaluación profunda de barreras, aumenta la frecuencia de coaching y considera coaching intensivo."
                                
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

# Tab 4: Desempeño
with tab4:
    st.write("<h2 style='text-align: center;'>📈 Puntaje de Desempeño</h2>", unsafe_allow_html=True)
    st.dataframe(df_desempeño, width='stretch', height=400)
    
    csv_desempeño = df_desempeño.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Desempeño en CSV",
        data=csv_desempeño,
        file_name=f"desempeño_datos_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Tab 5: Análisis por Métrica
with tab5:
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

# Tab 6: Leyenda de Métricas
with tab6:
    st.subheader("Leyenda de Métricas - Criterios y Puntajes")
    st.info("Esta tabla muestra todos los criterios de evaluación, sus descripciones, puntajes máximos y la categoría a la que pertenecen.")
    st.dataframe(df_metricas, width='stretch', height=600)
    
    csv_metricas = df_metricas.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Métricas en CSV",
        data=csv_metricas,
        file_name=f"metricas_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Tab 7: Niveles de Intensidad Sugeridos
with tab7:
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

# Tab 8: Control de Calidad
with tab8:
    st.write("<h2 style='text-align: center;'>📊 Control de Calidad</h2>", unsafe_allow_html=True)
    
    if not df_control_calidad.empty:
        st.dataframe(
            df_control_calidad,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No hay datos disponibles en el archivo de Control de Calidad.")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 20px;">
        <p>📊 Dashboard de Control de Auditorías | Actualizado: """ + datetime.now().strftime('%d/%m/%Y %H:%M') + """</p>
    </div>
""", unsafe_allow_html=True)
