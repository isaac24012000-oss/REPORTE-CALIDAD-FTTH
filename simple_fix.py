# Script de reemplazo directo - strings simples
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Reemplazos simples y directos
reemplazos = [
    ('# Tab 1: Datos de Control', '    # SubTab 1: Datos de Control'),
    ('with tab1:', '    with subtab1:'),
    
    ('# Tab 2: Plan de Acción', '    # SubTab 2: Plan de Acción'),
    ('with tab2:', '    with subtab2:'),
    
    ('# Tab 3: Progreso de Plan', '    # SubTab 3: Progreso de Plan'),
    ('with tab3:', '    with subtab3:'),
    
    ('# Tab 4: Desempeño', '    # SubTab 4: Desempeño'),
    ('with tab4:', '    with subtab4:'),
    
    ('# Tab 5: Análisis por Métrica', '    # SubTab 5: Análisis por Métrica'),
    ('with tab5:', '    with subtab5:'),
    
    ('# Tab 6: Leyenda de Métricas', '    # SubTab 6: Leyenda de Métricas'),
    ('with tab6:', '    with subtab6:'),
    
    ('# Tab 7: Niveles de Intensidad Sugeridos', '    # SubTab 7: Niveles de Intensidad Sugeridos'),
    ('with tab7:', '    with subtab7:'),
    
    ('# Tab 8: Control de Calidad', '# ==============================================\n# TAB CONTROL DE CALIDAD\n# =============================================='),
    ('with tab8:', 'with tab_control_calidad:'),
]

for buscar, reemplazar in reemplazos:
    contenido = contenido.replace(buscar, reemplazar)

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(contenido)

print("✅ Reemplazos completados")
