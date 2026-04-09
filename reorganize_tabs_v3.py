# Script para reorganizar tabs - versión funcional
import re

with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Paso 1: Reemplazar la declaración principal de tabs
tab_decl_old = r'# Tabs para diferentes vistas\ntab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st\.tabs\(\n    \["📋 Control de Auditorias", "📋 Plan de Acción", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad", "📊 Progreso de Plan", "📊 Control de Calidad"\]\n\)'

tab_decl_new = '''# Tabs principales: Monitoreo y Control de Calidad
tab_monitoreo, tab_control_calidad = st.tabs(
    ["📊 Monitoreo", "📊 Control de Calidad"]
)

# ==============================================
# TAB MONITOREO CON SUBTABS
# ==============================================
with tab_monitoreo:
    # Subtabs dentro de Monitoreo
    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6, subtab7 = st.tabs(
        ["📋 Control de Auditorias", "📋 Plan de Acción", "📈 Progreso de Plan", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad"]
    )'''

contenido = re.sub(tab_decl_old, tab_decl_new, contenido, flags=re.MULTILINE)

# Paso 2: Reemplazar cada "# Tab X:" con indentación y después el "with" correspondiente
# Tab 1: Datos de Control -> SubTab 1
contenido = re.sub(
    r'(\n)# Tab 1: Datos de Control\nwith tab1:',
    r'\1    # SubTab 1: Datos de Control\n    with subtab1:',
    contenido
)

# Tab 2: Plan de Acción -> SubTab 2
contenido = re.sub(
    r'(\n)# Tab 2: Plan de Acción\nwith tab2:',
    r'\1    # SubTab 2: Plan de Acción\n    with subtab2:',
    contenido
)

# Tab 3: Progreso de Plan -> SubTab 3
contenido = re.sub(
    r'(\n)# Tab 3: Progreso de Plan\nwith tab3:',
    r'\1    # SubTab 3: Progreso de Plan\n    with subtab3:',
    contenido
)

# Tab 4: Desempeño -> SubTab 4
contenido = re.sub(
    r'(\n)# Tab 4: Desempeño\nwith tab4:',
    r'\1    # SubTab 4: Desempeño\n    with subtab4:',
    contenido
)

# Tab 5: Análisis por Métrica -> SubTab 5
contenido = re.sub(
    r'(\n)# Tab 5: Análisis por Métrica\nwith tab5:',
    r'\1    # SubTab 5: Análisis por Métrica\n    with subtab5:',
    contenido
)

# Tab 6: Leyenda de Métricas -> SubTab 6
contenido = re.sub(
    r'(\n)# Tab 6: Leyenda de Métricas\nwith tab6:',
    r'\1    # SubTab 6: Leyenda de Métricas\n    with subtab6:',
    contenido
)

# Tab 7: Niveles de Intensidad Sugeridos -> SubTab 7
contenido = re.sub(
    r'(\n)# Tab 7: Niveles de Intensidad Sugeridos\nwith tab7:',
    r'\1    # SubTab 7: Niveles de Intensidad Sugeridos\n    with subtab7:',
    contenido
)

# Tab 8: Control de Calidad -> Tab principal (sin indentación)
contenido = re.sub(
    r'(\n)# Tab 8: Control de Calidad\nwith tab8:',
    r'\1# ==============================================\n# TAB CONTROL DE CALIDAD\n# ==============================================\nwith tab_control_calidad:',
    contenido
)

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(contenido)

print("✅ Primera fase completada - tabs y comentarios actualizados")
