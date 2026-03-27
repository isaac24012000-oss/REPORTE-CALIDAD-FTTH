from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__, template_folder='templates')

def colorear_valor(val, tipo_columna):
    """Agrega colores a los valores según el tipo de columna"""
    if pd.isna(val) or val == '-':
        return val
    
    val_str = str(val).strip()
    
    if tipo_columna == 'numero_impacto_desviacion':
        # Rojo si negativo, verde si positivo
        try:
            numero = float(val_str.replace('%', '').strip())
            if numero < 0:
                return f'<span style="color: #dc3545; font-weight: bold">{val_str}</span>'
            elif numero > 0:
                return f'<span style="color: #28a745; font-weight: bold">{val_str}</span>'
        except:
            pass
    
    elif tipo_columna == 'intensidad':
        # Rojo - Alta, Naranja - Media, Verde - Bajo
        val_lower = val_str.lower()
        if 'alta' in val_lower:
            return f'<span style="color: #dc3545; font-weight: bold">{val_str}</span>'
        elif 'media' in val_lower:
            return f'<span style="color: #fd7e14; font-weight: bold">{val_str}</span>'
        elif 'bajo' in val_lower or 'baja' in val_lower:
            return f'<span style="color: #28a745; font-weight: bold">{val_str}</span>'
    
    return val

# Columnas que queremos mostrar para la tabla Data
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

# Columnas que queremos mostrar para la tabla Couching
COLUMNAS_COUCHING = [
    'Agentes Zimach',
    'Sale Conv %',
    'Acción Principal',
    'Detalle de Trabajo'
]

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
    
    # Remover filas con etiquetas de resumen (Total, Sale Conversion %, etc.)
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
                        # Si ya contiene %, no multiplicar
                        if '%' in valor_str:
                            valor = float(valor_str.replace('%', ''))
                        else:
                            valor = float(valor_str) * 100
                        
                        # Redondear a 2 decimales para comparación
                        valor_redondeado = round(valor, 2)
                        
                        # Si es un número entero (sin decimales), mostrar sin decimales
                        if valor_redondeado == int(valor_redondeado):
                            return f'{int(valor_redondeado)}%'
                        return f'{valor_redondeado:.2f}%'
                    return '-'
                except (ValueError, TypeError):
                    return str(x)
            
            df_filtrado[col] = df_filtrado[col].apply(format_porcentaje)
    
    # Aplicar colores a columnas específicas
    df_filtrado['Impacto (%)'] = df_filtrado['Impacto (%)'].apply(lambda x: colorear_valor(x, 'numero_impacto_desviacion'))
    df_filtrado['Desviación'] = df_filtrado['Desviación'].apply(lambda x: colorear_valor(x, 'numero_impacto_desviacion'))
    df_filtrado['Intensidad'] = df_filtrado['Intensidad'].apply(lambda x: colorear_valor(x, 'intensidad'))
    
    return df_filtrado

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
                # Si ya contiene %, no multiplicar
                if '%' in valor_str:
                    valor = float(valor_str.replace('%', ''))
                else:
                    valor = float(valor_str) * 100
                
                # Redondear a 2 decimales para comparación
                valor_redondeado = round(valor, 2)
                
                # Si es un número entero (sin decimales), mostrar sin decimales
                if valor_redondeado == int(valor_redondeado):
                    return f'{int(valor_redondeado)}%'
                return f'{valor_redondeado:.2f}%'
            return '-'
        except (ValueError, TypeError):
            return str(x)
    
    df_filtrado['Sale Conv %'] = df_filtrado['Sale Conv %'].apply(format_porcentaje)
    
    return df_filtrado

def cargar_datos_metricas():
    """Carga y estructura los datos de la hoja Metricas"""
    excel_file = 'CONTROL DE AUDITORIAS.xlsx'
    df_metricas = pd.read_excel(excel_file, sheet_name='Metricas', header=None)
    
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
    
    # Ordenar por segmento y criterio
    df_resultado = df_resultado.sort_values(['Segmento', 'Criterio'])
    
    return df_resultado

def calcular_puntaje_desempeño():
    """Calcula el puntaje y porcentaje de desempeño para cada agente"""
    excel_file = 'CONTROL DE AUDITORIAS.xlsx'
    
    # Leer hoja Couching
    df_couching = pd.read_excel(excel_file, sheet_name='Couching')
    
    # Criterios evaluables (excluyendo columnas de resumen)
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
    
    # Extraer puntajes máximos de Metricas
    df_metricas = pd.read_excel(excel_file, sheet_name='Metricas', header=None)
    puntos_max = {}
    
    # Mapeo de criterios a columna de puntos en Metricas (aproximado basado en estructura)
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
        
        # Verificar si es una fila válida de agente Zimach
        if pd.isna(agente) or str(agente).strip() == '':
            continue
        
        agente_str = str(agente).strip()
        
        # Saltar filas especiales y mantener solo agentes Zimach válidos
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

@app.route('/')
def dashboard():
    """Renderiza el dashboard"""
    df = cargar_datos()
    df_couching = cargar_datos_couching()
    df_desempeño = calcular_puntaje_desempeño()
    df_metricas = cargar_datos_metricas()
    
    # Convertir DataFrames a HTML
    tabla_html = df.to_html(
        classes='table table-striped table-hover',
        index=False,
        escape=False
    )
    
    tabla_couching_html = df_couching.to_html(
        classes='table table-striped table-hover',
        index=False,
        escape=False
    )
    
    tabla_desempeño_html = df_desempeño.to_html(
        classes='table table-striped table-hover',
        index=False,
        escape=False
    )
    
    tabla_metricas_html = df_metricas.to_html(
        classes='table table-striped table-hover',
        index=False,
        escape=False
    )
    
    # Estadísticas (usar datos filtrados para cálculos correctos)
    total_agentes = len(df)
    
    # Multiplicar por 100 para convertir a porcentaje
    # Extraer valores numéricos de las columnas formateadas para el promedio
    excel_file = 'CONTROL DE AUDITORIAS.xlsx'
    df_raw = pd.read_excel(excel_file, sheet_name='Data')
    
    # Filtrar solo agentes Zimach en df_raw
    df_raw_filtrado = df_raw[df_raw['Agentes Zimach'].astype(str).str.contains('ZIM_', case=False, na=False)]
    
    conv_promedio = df_raw_filtrado['Sale Conv %'].mean() * 100
    calidad_promedio = df_raw_filtrado['% calidad'].mean() * 100
    
    # Formato sin decimales si es número entero
    if conv_promedio == int(conv_promedio):
        conv_str = f'{int(conv_promedio)}%'
    else:
        conv_str = f'{conv_promedio:.2f}%'
    
    if calidad_promedio == int(calidad_promedio):
        calidad_str = f'{int(calidad_promedio)}%'
    else:
        calidad_str = f'{calidad_promedio:.2f}%'
    
    return render_template(
        'dashboard.html',
        tabla=tabla_html,
        tabla_couching=tabla_couching_html,
        tabla_desempeño=tabla_desempeño_html,
        tabla_metricas=tabla_metricas_html,
        total_agentes=total_agentes,
        conv_promedio=conv_str,
        calidad_promedio=calidad_str
    )

@app.route('/api/puntaje-criterio/<path:criterio>')
def obtener_puntaje_criterio(criterio):
    """API para obtener puntajes de un criterio específico"""
    try:
        import urllib.parse
        criterio_decodificado = urllib.parse.unquote(criterio)
        
        # Mapeo de puntajes máximos por criterio
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
        
        excel_file = 'CONTROL DE AUDITORIAS.xlsx'
        df_couching = pd.read_excel(excel_file, sheet_name='Couching')
        
        # Buscar la columna exacta
        criterio_encontrado = None
        for col in df_couching.columns:
            if col.strip() == criterio_decodificado.strip():
                criterio_encontrado = col
                break
        
        if not criterio_encontrado:
            return jsonify({'error': f'Criterio no encontrado: {criterio_decodificado}'}), 404
        
        # Obtener puntaje máximo
        puntaje_maximo = puntos_maximos.get(criterio_encontrado, 'N/A')
        
        resultados = []
        
        for idx, row in df_couching.iterrows():
            agente = str(row['Agentes Zimach']).strip()
            
            # Saltar filas vacías, "nan", o de resumen
            if not agente or agente.lower() in ['total', 'sale conversion %', 'nan']:
                continue
            
            # Solo incluir agentes Zimach válidos
            if 'ZIM_' not in agente.upper():
                continue
            
            try:
                valor = row[criterio_encontrado]
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
                        
                        # Calcular porcentaje
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
        
        if not resultados:
            return jsonify({'error': 'No hay datos disponibles'}), 404
        
        df_resultado = pd.DataFrame(resultados)
        tabla_html = df_resultado.to_html(classes='table table-striped table-hover', index=False, escape=False)
        
        return jsonify({
            'tabla': tabla_html, 
            'criterio': criterio_encontrado,
            'puntaje_maximo': puntaje_maximo,
            'estado': 'exito'
        })
    
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Dashboard iniciado en: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='localhost', port=5000)
