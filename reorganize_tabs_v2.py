# Script avanzado para reorganizar tabs con indentación correcta
import re

with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Encontrar línea donde comienza "# Tabs para diferentes vistas"
inicio_tabs = None
for i, linea in enumerate(lineas):
    if '# Tabs para diferentes vistas' in linea:
        inicio_tabs = i
        break

if inicio_tabs is None:
    print("❌ No se encontró la sección de tabs")
    exit(1)

# Procesar: 
# 1. Reemplazar la declaración de tabs (3 líneas)
# 2. Insertar la nueva estructura y el `with tab_monitoreo:`
# 3. Indentación de cada bloque with tabX

# Buscar las líneas exactas
fin_declaracion = inicio_tabs + 3  # "# Tabs...", "tab1, tab2...", "[...]"

# Línea donde comienza "# Tab 1:"
inicio_tab1 = None
for i in range(fin_declaracion, len(lineas)):
    if '# Tab 1: Datos de Control' in lineas[i]:
        inicio_tab1 = i
        break

if inicio_tab1 is None:
    print("❌ No se encontró # Tab 1")
    exit(1)

# Construir la salida
salida = []

# Copiar hasta antes de "# Tabs para diferentes vistas"
salida.extend(lineas[:inicio_tabs])

# Agregar nueva declaración de tabs
salida.append('# Tabs principales: Monitoreo y Control de Calidad\n')
salida.append('tab_monitoreo, tab_control_calidad = st.tabs(\n')
salida.append('    ["📊 Monitoreo", "📊 Control de Calidad"]\n')
salida.append(')\n')
salida.append('\n')
salida.append('# ==============================================\n')
salida.append('# TAB MONITOREO CON SUBTABS\n')
salida.append('# ==============================================\n')
salida.append('with tab_monitoreo:\n')
salida.append('    # Subtabs dentro de Monitoreo\n')
salida.append('    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6, subtab7 = st.tabs(\n')
salida.append('        ["📋 Control de Auditorias", "📋 Plan de Acción", "📈 Progreso de Plan", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad"]\n')
salida.append('    )\n')
salida.append('\n')

# Ahora procesar cada bloque with tabX: -> with subtabX: con indentación
linea_actual = inicio_tab1
tab_num = 1
contador_tab = 1

while linea_actual < len(lineas):
    linea = lineas[linea_actual]
    
    # Detectar inicio de nuevo tab
    if linea_actual > inicio_tab1 and f'# Tab {contador_tab}:' in linea:
        # Éste es el inicio de un nuevo bloque de tab
        # Si es Tab 8, debe ir a tab_control_calidad, no a subtab8
        if contador_tab == 8:
            salida.append('\n')
            salida.append('# ==============================================\n')
            salida.append('# TAB CONTROL DE CALIDAD\n')
            salida.append('# ==============================================\n')
            # Siguiente línea debe ser "with tab8:"
            linea_actual += 1
            salida.append('with tab_control_calidad:\n')
            contador_tab += 1
        else:
            # Es uno de los tabs 1-7, que van como subtabs
            salida.append('    # SubTab ' + str(contador_tab) + ': ' + linea.split(': ')[1] if ': ' in linea else 'SubTab')
            linea_actual += 1
            # Siguiente línea debe ser "with tabX:"
            if col_actual < len(lineas) and 'with tab' + str(contador_tab) + ':' in lineas[linea_actual]:
                salida.append('    with subtab' + str(contador_tab) + ':\n')
                linea_actual += 1
                contador_tab += 1
            else:
                salida.append(linea)
                linea_actual += 1
    else:
        # Línea de contenido dentro de un bloque
        # Si el contador_tab < 8, necesita indentación adicional
        if contador_tab <= 7 and linea_actual > inicio_tab1:
            # Añadir 4 espacios al inicio si already tiene spaces
            if linea.strip() and not linea.startswith('# Tab') and not linea.startswith('with tab'):
                if linea.startswith('    '):
                    salida.append('    ' + linea)  # Agregar 4 espacios más
                elif linea.startswith('\n'):
                    salida.append(linea)
                else:
                    salida.append('    ' + linea)
            else:
                salida.append(linea)
        else:
            salida.append(linea)
        
        linea_actual += 1

# Escribir el archivo
with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.writelines(salida)

print("✅ Script completado - procesamiento de tabs")
