# Script definitivo - reestructura con bloque with correcto
import re

with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Encontrar dónde inicia el bloque de tabs
match = re.search(r'(# Tabs para diferentes vistas.*)', contenido, re.DOTALL)
if not match:
    print("❌ No se encontró la sección de tabs")
    exit(1)

inicio_seccion = match.start()
anterior = contenido[:inicio_seccion]
seccion_tabs = contenido[inicio_seccion:]

# Función para extraer contenido d cada tab
def extraer_tab(contenido_txt, numero_tab, es_ultimo=False):
    if es_ultimo:
        # Tab 8 va hasta EOF
        patron = rf'with tab{numero_tab}:(.*?)$'
    else:
        # Los demás van hasta el siguiente # Tab
        patron = rf'with tab{numero_tab}:(.*?)(?=\n# Tab {numero_tab + 1}:)'
    
    match = re.search(patron, contenido_txt, re.DOTALL)
    if match:
        content = match.group(1)
        # Indentamos cada línea agregando 8 espacios (para subtabs)
        # EXCEPTO la última línea vacía
        lineas = content.split('\n')
        resultado = []
        for linea in lineas:
            if linea.strip():  # No es vacía
                resultado.append('        ' + linea)
            else:
                resultado.append(linea)
        return '\n'.join(resultado)
    return ""

# Construir nueva estructura
nueva = '''# Tabs principales: Monitoreo y Control de Calidad
tab_monitoreo, tab_control_calidad = st.tabs(
    ["📊 Monitoreo", "📊 Control de Calidad"]
)

# ==============================================
# TAB MONITOREO
# ==============================================
with tab_monitoreo:
    # Subtabs dentro de Monitoreo
    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6, subtab7 = st.tabs(
        ["📋 Control de Auditorias", "📋 Plan de Acción", "📈 Progreso de Plan", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad"]
    )
'''

# Agregar cada tab como subtab
for i in range(1, 8):
    nueva += f'\n    # SubTab {i}:\n    with subtab{i}:\n'
    contenido_tab_i = extraer_tab(seccion_tabs, i, es_ultimo=False)
    nueva += contenido_tab_i

# Tab 8 - Control de Calidad (sin anidación, a nivel raíz)
nueva += '''\n# ==============================================
# TAB CONTROL DE CALIDAD
# ==============================================
with tab_control_calidad:
'''
contenido_tab8_indentado = extraer_tab(seccion_tabs, 8, es_ultimo=True)
# Desindentar para tab_control_calidad (va a nivel 0, solo con indent if dentro)
lineas_tab8 = contenido_tab8_indentado.split('\n')
for linea in lineas_tab8:
    if linea.startswith('        '):  # Tiene 8 espacios de los subtabs
        # Remover 4 para dejar solo 4 (contenido de tab_control_calidad)
        nueva += '\n' + linea[4:]
    else:
        nueva += '\n' + linea

# Escribir
resultado_final = anterior + nueva
with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(resultado_final)

print("✅ Reestructuración completa")
