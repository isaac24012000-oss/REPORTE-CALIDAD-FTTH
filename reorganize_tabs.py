# Script para reorganizar tabs
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# 1. Reemplazar la declaración de tabs
old_tabs_declaration = '''# Tabs para diferentes vistas
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    ["📋 Control de Auditorias", "📋 Plan de Acción", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad", "📊 Progreso de Plan", "📊 Control de Calidad"]
)'''

new_tabs_declaration = '''# Tabs principales: Monitoreo y Control de Calidad
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

contenido = contenido.replace(old_tabs_declaration, new_tabs_declaration)

# 2. Reemplazar "# Tab 1:" con "# SubTab 1:" y con indentación
contenido = contenido.replace("# Tab 1: Datos de Control\nwith tab1:", "    # SubTab 1: Datos de Control\n    with subtab1:")
contenido = contenido.replace("# Tab 2: Plan de Acción\nwith tab2:", "    # SubTab 2: Plan de Acción\n    with subtab2:")
# Tab 3 es Progreso de Plan (va a ser subtab3)
contenido = contenido.replace("# Tab 3: Progreso de Plan\nwith tab3:", "    # SubTab 3: Progreso de Plan\n    with subtab3:")
# Tab 4 es Desempeño (va a ser subtab4)
contenido = contenido.replace("# Tab 4: Desempeño\nwith tab4:", "    # SubTab 4: Desempeño\n    with subtab4:")
# Tab 5 es Análisis por Métrica (va a ser subtab5)
contenido = contenido.replace("# Tab 5: Análisis por Métrica\nwith tab5:", "    # SubTab 5: Análisis por Métrica\n    with subtab5:")
# Tab 6 es Leyenda de Métricas (va a ser subtab6)
contenido = contenido.replace("# Tab 6: Leyenda de Métricas\nwith tab6:", "    # SubTab 6: Leyenda de Métricas\n    with subtab6:")
# Tab 7 es Niveles de Intensidad (va a ser subtab7)
contenido = contenido.replace("# Tab 7: Niveles de Intensidad Sugeridos\nwith tab7:", "    # SubTab 7: Niveles de Intensidad Sugeridos\n    with subtab7:")
# Tab 8 es Control de Calidad (va a ser tab_control_calidad, sin subtabs)
contenido = contenido.replace("# Tab 8: Control de Calidad\nwith tab8:", "\n# ==============================================\n# TAB CONTROL DE CALIDAD\n# ==============================================\nwith tab_control_calidad:")

# Escribir el archivo modificado
with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(contenido)

print("✅ Archivo modificado exitosamente - estructura de tabs reorganizada")
