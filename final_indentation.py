# Script FINAL - Duplica indentación correctamente dentro de subtabs
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    lineas = f.readlines()

salida = []
dentro_subtab = False
en_seccion_monitoreo = False

for i, linea in enumerate(lineas):
    # Detectar entrada a sección Monitoreo
    if 'with tab_monitoreo:' in linea:
        en_seccion_monitoreo = True
        salida.append(linea)
        continue
    
    # Detectar entrada a subtab
    if 'with subtab' in linea and en_seccion_monitoreo:
        dentro_subtab = True
        salida.append(linea)
        continue
    
    # Detectar salida de subtab
    if dentro_subtab and (linea.strip().startswith('# SubTab') or linea.strip().startswith('with tab_control')):
        dentro_subtab = False
        if linea.strip().startswith('with tab_control'):
            en_seccion_monitoreo = False
    
    # Procesamiento de línea
    if dentro_subtab and linea.strip():  # Dentro de subtab AND no línea vacía
        # Contar espacios iniciales
        espacios = len(linea) - len(linea.lstrip())
        contenido = linea.lstrip()
        
        # Duplicar espacios (pero máximo 8 original se convierte en 12)
        # 0 espacios -> 4; 4 espacios -> 8; 8 espacios -> 12; etc
        nuevos_espacios = espacios + 4
        
        salida.append(' ' * nuevos_espacios + contenido)
    else:
        salida.append(linea)

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.writelines(salida)

print("✅ Indentación FINAL aplicada")
