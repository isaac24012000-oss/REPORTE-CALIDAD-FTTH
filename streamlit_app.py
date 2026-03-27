import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

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
    '% calidad',
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
    excel_file = 'CONTROL DE AUDITORIAS.xlsx'
    df = pd.read_excel(excel_file, sheet_name='Data')
    
    # Seleccionar solo las columnas deseadas
    df_filtrado = df[COLUMNAS_MOSTRAR].copy()
    
    # Renombrar columnas para mejor legibilidad
    df_filtrado.columns = [
        'Agentes Zimach',
        'Sale Conv %',
        '% Calidad',
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
        '% Calidad',
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
    excel_file = 'CONTROL DE AUDITORIAS.xlsx'
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
    excel_file = 'CONTROL DE AUDITORIAS.xlsx'
    
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
    excel_file = 'CONTROL DE AUDITORIAS.xlsx'
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

# Cargar datos
df_data = cargar_datos()
df_couching = cargar_datos_couching()
df_desempeño = calcular_puntaje_desempeño()
df_metricas = cargar_datos_metricas()

# Cálculos para estadísticas
excel_file = 'CONTROL DE AUDITORIAS.xlsx'
df_raw = pd.read_excel(excel_file, sheet_name='Data')
df_raw_filtrado = df_raw[df_raw['Agentes Zimach'].astype(str).str.contains('ZIM_', case=False, na=False)]

total_agentes = len(df_data)
conv_promedio = df_raw_filtrado['Sale Conv %'].mean() * 100
calidad_promedio = df_raw_filtrado['% calidad'].mean() * 100

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
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📋 Control", "📋 Plan de Acción", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas"]
)

# Tab 1: Datos de Control
with tab1:
    st.write("<h2 style='text-align: center;'>📋 Control de Auditorías</h2>", unsafe_allow_html=True)
    
    # Aplicar colores al DataFrame
    df_coloreado = aplicar_colores_df(df_data)
    
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
    csv_data = df_data.to_csv(index=False).encode('utf-8')
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

# Tab 3: Desempeño
with tab3:
    st.write("<h2 style='text-align: center;'>📈 Puntaje de Desempeño</h2>", unsafe_allow_html=True)
    st.dataframe(df_desempeño, width='stretch', height=400)
    
    csv_desempeño = df_desempeño.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Desempeño en CSV",
        data=csv_desempeño,
        file_name=f"desempeño_datos_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Tab 4: Análisis por Métrica
with tab4:
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
        excel_file = 'CONTROL DE AUDITORIAS.xlsx'
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
                st.write(f"**Criterio:** {criterio_seleccionado}")
                st.write(f"**Puntaje Máximo:** {puntaje_maximo}")
                st.dataframe(df_resultado, width='stretch')
                
                csv_criterio = df_resultado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar en CSV",
                    data=csv_criterio,
                    file_name=f"{criterio_seleccionado}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

# Tab 5: Leyenda de Métricas
with tab5:
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

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 20px;">
        <p>📊 Dashboard de Control de Auditorías | Actualizado: """ + datetime.now().strftime('%d/%m/%Y %H:%M') + """</p>
    </div>
""", unsafe_allow_html=True)
