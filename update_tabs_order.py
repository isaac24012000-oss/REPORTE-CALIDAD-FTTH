#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Leer el archivo
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazar la lista de tabs - buscar y reemplazar directamente
old_line = '    ["📋 Control", "📋 Plan de Acción", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad", "📈 Progreso de Plan"]'
new_line = '    ["📋 Control", "📋 Plan de Acción", "📈 Progreso de Plan", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad"]'

# Hacer el reemplazo
if old_line in content:
    content = content.replace(old_line, new_line)
    print("✅ Lista de tabs actualizada")
else:
    print("⚠️ No se encontró la línea exacta de tabs")
    # Intentar una búsqueda parcial
    if '"📋 Control"' in content and '"📈 Desempeño"' in content and '"📈 Progreso de Plan"' in content:
        # Buscar el patrón y reemplazar
        import re
        pattern = r'\["📋 Control".*?"📈 Progreso de Plan"\]'
        replacement = '["📋 Control", "📋 Plan de Acción", "📈 Progreso de Plan", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad"]'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print("✅ Lista de tabs actualizada con regex")

# Escribir el archivo de vuelta
with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Archivo guardado")
