# Script para fijar los reemplazos - trabaja con líneas directamente
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Reemplazos con regex que entienda newlines reales
import re

# Reemplazar "# Tab 1: Datos de Control" seguido de "with tab1:"
contenido = re.sub(
    r'(\A|\n)(# Tab 1: Datos de Control)\n(with tab1:)',
    r'\1    # SubTab 1: Datos de Control\n    with subtab1:',
    contenido
)

# TAB 2
contenido = re.sub(
    r'\n(# Tab 2: Plan de Acción)\n(with tab2:)',
    r'\n    # SubTab 2: Plan de Acción\n    with subtab2:',
    contenido
)

# TAB 3
contenido = re.sub(
    r'\n(# Tab 3: Progreso de Plan)\n(with tab3:)',
    r'\n    # SubTab 3: Progreso de Plan\n    with subtab3:',
    contenido
)

# TAB 4
contenido = re.sub(
    r'\n(# Tab 4: Desempeño)\n(with tab4:)',
    r'\n    # SubTab 4: Desempeño\n    with subtab4:',
    contenido
)

# TAB 5
contenido = re.sub(
    r'\n(# Tab 5: Análisis por Métrica)\n(with tab5:)',
    r'\n    # SubTab 5: Análisis por Métrica\n    with subtab5:',
    contenido
)

# TAB 6
contenido = re.sub(
    r'\n(# Tab 6: Leyenda de Métricas)\n(with tab6:)',
    r'\n    # SubTab 6: Leyenda de Métricas\n    with subtab6:',
    contenido
)

# TAB 7
contenido = re.sub(
    r'\n(# Tab 7: Niveles de Intensidad Sugeridos)\n(with tab7:)',
    r'\n    # SubTab 7: Niveles de Intensidad Sugeridos\n    with subtab7:',
    contenido
)

# TAB 8
contenido = re.sub(
    r'\n(# Tab 8: Control de Calidad)\n(with tab8:)',
    r'\n# ==============================================\n# TAB CONTROL DE CALIDAD\n# ==============================================\nwith tab_control_calidad:',
    contenido
)

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(contenido)

print("✅ Reemplazos aplicados correctamente")
