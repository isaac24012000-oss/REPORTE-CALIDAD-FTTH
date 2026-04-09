# Script para cambios de terminología
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Reemplazos simples
contenido = contenido.replace("'📈 Subiendo fuerte'", "'📈 En Aumento'")
contenido = contenido.replace("'📈 Subiendo poquito'", "'📈 En Aumento'")
contenido = contenido.replace("'😌 Tranquilo (casi sin cambios)'", "'↔️ Mantiene Nivel'")
contenido = contenido.replace("'😌 Tranquilo'", "'↔️ Mantiene Nivel'")
contenido = contenido.replace("'📉 Bajando'", "'📉 En Disminución'")

# También en los títulos
contenido = contenido.replace('"Subiendo fuerte"', '"En Aumento"')
contenido = contenido.replace('"Subiendo poquito"', '"En Aumento"')
contenido = contenido.replace('"Tranquilo"', '"Mantiene Nivel"')
contenido = contenido.replace('"Bajando"', '"En Disminución"')

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(contenido)

print("✅ Todos los cambios aplicados correctamente")
