# 📊 Dashboard - Control de Auditorías

Sistema de análisis y evaluación de desempeño de agentes con métricas de calidad, conversión e intensidad.

## 🎯 Características

- ✅ **Análisis de Auditorías**: Datos detallados de desempeño de agentes
- ✅ **Indicadores de Couching**: Métricas especializadas por criterio
- ✅ **Puntaje de Desempeño**: Evaluación integral de cada agente
- ✅ **Análisis por Criterio**: Filtro detallado de métricas individuales
- ✅ **Colorización Automática**: Código de colores para impacto y desviación
- ✅ **Descarga de Datos**: Exportación a CSV de todos los reportes
- ✅ **Interfaz Responsiva**: Acceso desde cualquier dispositivo

## 📋 Opciones de Ejecución

Tienes 2 formas de usar este dashboard:

### 1️⃣ **Opción 1: Streamlit (Recomendado para compartir)**

Streamlit es más fácil de compartir y no requiere configuración web avanzada.

#### Instalación inicial:
```bash
# Navegar a la carpeta del proyecto
cd "c:\Users\USUARIO\Desktop\REPORTE DE CALIDAD"

# Instalar dependencias
pip install -r requirements.txt
```

#### Ejecutar la aplicación:
```bash
streamlit run streamlit_app.py
```

La aplicación se abrirá en `http://localhost:8501`

#### Compartir Streamlit Cloud (Gratis):
1. Subir los archivos a GitHub
2. Conectar el repositorio en [Streamlit Cloud](https://streamlit.io/cloud)
3. Compartir el enlace público con tu equipo

---

### 2️⃣ **Opción 2: Flask (Desarrollo/Producción)**

Para usar la versión web más tradicional.

#### Ejecutar la aplicación:
```bash
# Navegar a la carpeta del proyecto
cd "c:\Users\USUARIO\Desktop\REPORTE DE CALIDAD"

# Ejecutar Flask
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

---

## 🎨 Colores Utilizados

### Impacto (%)
- 🔴 **Rojo**: Valores negativos (impacto negativo)
- 🟢 **Verde**: Valores positivos (mejora)

### Desviación
- 🔴 **Rojo**: Valores negativos (por debajo de meta)
- 🟢 **Verde**: Valores positivos (por encima de meta)

### Intensidad
- 🔴 **Rojo**: "Alta" (máxima carga)
- 🟠 **Naranja**: "Media" (carga moderada)
- 🟢 **Verde**: "Bajo" (baja carga)

---

## 📁 Estructura del Proyecto

```
REPORTE DE CALIDAD/
├── app.py                      # Aplicación Flask
├── streamlit_app.py           # Aplicación Streamlit
├── requirements.txt            # Dependencias Python
├── CONTROL DE AUDITORIAS.xlsx  # Archivo de datos
├── templates/
│   └── dashboard.html         # Plantilla HTML para Flask
└── README.md                  # Este archivo
```

---

## 📊 Datos Cargados

El dashboard carga datos de 3 hojas del archivo Excel:

### 1. **Data Sheet**
Contiene información básica de auditorías:
- Agentes Zimach
- Sale Conv %
- % Calidad
- Intensidad
- Metas (S1-S4)
- Impacto (%)
- Desviación

### 2. **Couching Sheet**
Evaluación especializada por criterios:
- 19 criterios de evaluación
- Puntajes de 1-12 por criterio
- Máximo 119 puntos totales

### 3. **Metricas Sheet**
Referencias y descripciones de criterios

---

## 🔍 Criterios de Evaluación (19 Total)

### Habilidades de Apertura (5 criterios)
- Presentación
- Expresión Verbal / Dicción
- Tiempo de Espera
- Validación de Titular
- Sondeo Asertivo

### Diagnóstico y Perfilamiento (3 criterios)
- Identificación de Necesidad
- Capacidad de Pago / Interés Real
- Detección de Decisor

### Negociación (5 criterios)
- Escucha Activa
- Manejo de Llamada
- Seguridad
- Empatía
- Negociación Escalonada

### Argumentación Comercial (3 criterios)
- Beneficios Claros
- Diferenciación vs Competencia
- Personalización del Discurso

### Cierre de Llamada (3 criterios)
- Generación de Urgencia
- Registro en Sistema
- Uso de Etiquetas

---

## 📊 Estadísticas Principales

El dashboard muestra 3 métricas clave:
- **Total de Agentes**: Número de agentes Zimach activos
- **Conversión Promedio**: Porcentaje promedio de conversión
- **Calidad Promedio**: Porcentaje promedio de calidad

---

## ⚙️ Requisitos Técnicos

- Python 3.8+
- Pandas 2.0+
- Streamlit 1.28+
- Flask 3.0+
- openpyxl 3.1+

---

## 🚀 Pasos para Compartir

### Opción A: Streamlit Cloud (Recomendado)
```
1. Crear cuenta en streamlit.io
2. Conectar repositorio GitHub
3. Seleccionar deployar streamlit_app.py
4. Compartir URL público
```

### Opción B: Ejecutar localmente
```
1. Instalar Python 3.8+
2. Clonar repositorio
3. pip install -r requirements.txt
4. streamlit run streamlit_app.py
5. Compartir IP local + puerto (8501)
```

### Opción C: Servidor Docker
```
1. Crear Dockerfile
2. docker build -t dashboard .
3. docker run -p 8501:8501 dashboard
```

---

## 🐛 Solución de Problemas

**Error: "FileNotFoundError: CONTROL DE AUDITORIAS.xlsx"**
- Verificar que el archivo Excel está en la misma carpeta que los scripts

**Error: "ModuleNotFoundError"**
- Ejecutar: `pip install -r requirements.txt`

**Streamlit no inicia**
- Verificar: `streamlit --version`
- Reinstalar: `pip install --upgrade streamlit`

---

## 📝 Notas Importantes

- Los datos se cargan del Excel automáticamente
- Solo se muestran agentes con prefijo "ZIM_"
- Las métricas se actualizan al refrescar la página
- Los CSV descargados incluyen la fecha actual

---

## 📧 Soporte

Para consultas o reportar problemas, contactar al equipo de desarrollo.

---

**Última actualización:** 27 de Marzo, 2026
**Versión:** 1.0
