# Script simple - reemplazos directos sin re-indentación
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Encontrar la línea donde declara los tabs
for i, linea in enumerate(lineas):
    if 'tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs' in linea:
        # Reemplazar esa seccion completamente
        # Encontrar el cierre de los paréntesis ]
        j = i
        while j < len(lineas) and ')' not in lineas[j]:
            j += 1
        
        # Insertar nueva estructura antes de i
        nuevas_lineas = [
            '# Tabs principales: Monitoreo y Control de Calidad\n',
            'tab_monitoreo, tab_control_calidad = st.tabs(\n',
            '    ["📊 Monitoreo", "📊 Control de Calidad"]\n',
            ')\n',
            '\n',
            '# ==============================================\n',
            '# TAB MONITOREO\n',
            '# ==============================================\n',
            'with tab_monitoreo:\n',
            '    # Subtabs dentro de Monitoreo\n',
            '    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6, subtab7 = st.tabs(\n',
            '        ["📋 Control de Auditorias", "📋 Plan de Acción", "📈 Progreso de Plan", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad"]\n',
            '    )\n',
        ]
        
        # Reemplazar desde i hasta j (inclusive)
        lineas = lineas[:i] + nuevas_lineas + lineas[j+1:]
        break

# Después reemplazamos los with tab#: 
resultado = '\n'.join(lineas)

# Reemplazos simples sin cambiar indentación
reemplazos = [
    ('# Tab 1: Datos de Control\nwith tab1:', '    # SubTab 1: Datos de Control\n    with subtab1:'),
    ('# Tab 2: Plan de Acción\nwith tab2:', '    # SubTab 2: Plan de Acción\n    with subtab2:'),
    ('# Tab 3: Progreso de Plan\nwith tab3:', '    # SubTab 3: Progreso de Plan\n    with subtab3:'),
    ('# Tab 4: Desempeño\nwith tab4:', '    # SubTab 4: Desempeño\n    with subtab4:'),
    ('# Tab 5: Análisis por Métrica\nwith tab5:', '    # SubTab 5: Análisis por Métrica\n    with subtab5:'),
    ('# Tab 6: Leyenda de Métricas\nwith tab6:', '    # SubTab 6: Leyenda de Métricas\n    with subtab6:'),
    ('# Tab 7: Niveles de Intensidad Sugeridos\nwith tab7:', '    # SubTab 7: Niveles de Intensidad Sugeridos\n    with subtab7:'),
    ('# Tab 8: Control de Calidad\nwith tab8:', '\n# ==============================================\n# TAB CONTROL DE CALIDAD\n# ==============================================\nwith tab_control_calidad:'),
]

for buscar, reemplazar in reemplazos:
    resultado = resultado.replace(buscar, reemplazar)

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(resultado)

print("✅ Cambios aplicados")
