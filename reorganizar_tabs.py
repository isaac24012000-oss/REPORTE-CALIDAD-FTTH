import re

# Leer el archivo
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar y reemplazar la línea de tabs
for i, line in enumerate(lines):
    if 'tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(' in line:
        # Reemplazar las próximas líneas que contienen la definición de tabs
        if i + 1 < len(lines) and '["📋 Control"' in lines[i + 1]:
            lines[i + 1] = '    ["📋 Control", "📋 Plan de Acción", "📈 Progreso de Plan", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad"]\n'
            break

# Escribir el archivo actualizado
with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Archivo actualizado")

