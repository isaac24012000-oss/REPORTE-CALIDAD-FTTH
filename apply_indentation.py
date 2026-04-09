# Script para indentación correcta post reemplazo de names
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Procesar línea por línea
salida = []
dentro_subtab = False

for i, linea in enumerate(lineas):
    # Detectar inicio de subtab
    if linea.strip().startswith('with subtab'):
        dentro_subtab = True
        salida.append(linea)
        continue
    
    # Detectar fin de subtab
    if dentro_subtab and (linea.strip().startswith('# =') or linea.strip().startswith('with tab_control')):
        dentro_subtab = False
    
    # Si estamos dentro de un subtab y la línea tiene contenido, indentamos 
    if dentro_subtab and linea.strip():
        # Contar espacios al inicio
        num_espacios = len(linea) - len(linea.lstrip(' '))
        
        # Solo indentamos líneas que comienzan con EXACTAMENTE 4 espacios
        if num_espacios == 4:
            # Agregar 4 espacios más
            salida.append('    ' + linea)
        elif num_espacios == 0:
            # Líneas sin espacios - agregar 8 (probablemente comentarios en el bloque del with)
            salida.append('        ' + linea)
        else:
            # Líneas ya indentadas más de 4 espacios (dentro de if, for, etc) - dejar como está
            salida.append(linea)
    else:
        # Línea vacía - dejar como está
        salida.append(linea)

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.writelines(salida)

print("✅ Indentación aplicada correctamente")
