# Script para reorganizar tabs
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Cambio 1: Actualizar la lista de tabs
content = content.replace(
    '["📋 Control", "📋 Plan de Acción", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad", "📈 Progreso de Plan"]',
    '["📋 Control", "📋 Plan de Acción", "📈 Progreso de Plan", "📈 Desempeño", "🔍 Análisis por Métrica", "📚 Métricas", "🎯 Niveles de Intensidad"]'
)

# Cambio 2: Tab 3 a Tab 4 (Desempeño)
content = content.replace('# Tab 3: Desempeño\nwith tab3:\n    st.write("<h2', '# Tab 4: Desempeño\nwith tab4:\n    st.write("<h2')

# Cambio 3: Tab 4 a Tab 5 (Análisis)
content = content.replace('# Tab 4: Análisis por Métrica\nwith tab4:\n    st.subheader', '# Tab 5: Análisis por Métrica\nwith tab5:\n    st.subheader')

# Cambio 4: Tab 5 a Tab 6 (Leyenda)
content = content.replace('# Tab 5: Leyenda de Métricas\nwith tab5:\n    st.subheader', '# Tab 6: Leyenda de Métricas\nwith tab6:\n    st.subheader')

# Cambio 5: Tab 6 a Tab 7 (Niveles)
content = content.replace('# Tab 6: Niveles de Intensidad Sugeridos\nwith tab6:\n    st.write', '# Tab 7: Niveles de Intensidad Sugeridos\nwith tab7:\n    st.write')

# Cambio 6: Tab 7 a Tab 3 (Progreso)
content = content.replace('# Tab 7: Progreso de Plan\nwith tab7:\n    st.write', '# Tab 3: Progreso de Plan\nwith tab3:\n    st.write')

# Cambio 7: tab7_diaria a tab3_diaria y tab7_semanal a tab3_semanal
content = content.replace('tab7_diaria, tab7_semanal', 'tab3_diaria, tab3_semanal')
content = content.replace('with tab7_diaria:', 'with tab3_diaria:')
content = content.replace('with tab7_semanal:', 'with tab3_semanal:')

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Reorganización completada")
