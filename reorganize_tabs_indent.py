# Script para indentación correcta de contenido dentro de subtabs
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Identificar líneas donde empiezan los bloques with subtab y with tab_control_calidad
bloques = []  # Lista de (inicio_linea, tipo, numero)

for i, linea in enumerate(lineas):
    if linea.strip().startswith('with subtab'):
        # Extraer número
        num = linea.split('subtab')[1].split(':')[0]
        bloques.append((i, 'subtab', int(num)))
    elif linea.strip().startswith('with tab_control_calidad:'):
        bloques.append((i, 'control_calidad', 8))

print(f"Encontrados {len(bloques)} bloques")
for i, t, n in bloques[:3]:
    print(f"  Línea {i}: {t} {n}")

# Ahora, para cada bloque
salida = []
i = 0

while i < len(lineas):
    linea = lineas[i]
    salida.append(linea)
    
    # Si esta línea inicia un bloque with subtab, indentamos hasta el próximo with
    if linea.strip().startswith('with subtab') or linea.strip().startswith('with tab_control_calidad'):
        i += 1
        # Indentamos todo hasta la siguiente línea tipo "with subtab/tab_control_calidad" O "# SubTab" OR "# Tab" o EOF
        while i < len(lineas):
            siguiente = lineas[i]
            
            # Detectar si es el inicio del próximo bloque
            if (siguiente.strip().startswith('with subtab') or 
                siguiente.strip().startswith('with tab_control_calidad') or
                siguiente.strip().startswith('# SubTab') or
                siguiente.strip().startswith('# Tab') or
                siguiente.strip().startswith('# ===')):
                # No agregar indentación, solo salir del loop
                break
            
            # Indentación lógica: Si la línea tiene contenido (no está vacía), agregar 4 espacios
            if siguiente.strip():  # Línea NO vacía
                if not siguiente.startswith('        '):  # No está ya profundamente indentada
                    salida.append('    ' + siguiente)
                else:
                    salida.append(siguiente)
            else:
                salida.append(siguiente)
            
            i += 1
        continue
    
    i += 1

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.writelines(salida)

print("✅ Segunda fase completada - indentación aplicada")
