# 📚 Guía de Instalación Detallada

## ✅ Opción 1: Instalación Automática (Windows)

Hemos creado scripts que hacen todo automáticamente.

### Paso 1: Ejecutar instalación
1. Navega a la carpeta del proyecto
2. Haz doble clic en **`install.bat`**
3. Espera a que termine (verá mensajes de éxito)

### Paso 2: Iniciar la aplicación

**Para Streamlit (Recomendado):**
- Doble clic en **`run_streamlit.bat`**
- Se abrirá automáticamente en http://localhost:8501

**Para Flask:**
- Doble clic en **`run_flask.bat`**
- Acceder a http://localhost:5000 en el navegador

---

## ✅ Opción 2: Instalación Manual

Si prefieres o los scripts no funcionan.

### Paso 1: Verificar Python
```bash
python --version
```
Debe mostrar Python 3.8 o superior. Si no está instalado, descárgalo desde https://www.python.org/

### Paso 2: Crear entorno virtual
```bash
python -m venv .venv
```

### Paso 3: Activar entorno virtual

**En Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**En Mac/Linux:**
```bash
source .venv/bin/activate
```

### Paso 4: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 5: Ejecutar aplicación

**Streamlit:**
```bash
streamlit run streamlit_app.py
```

**Flask:**
```bash
python app.py
```

---

## ✅ Opción 3: Docker (Avanzado)

Si tienes Docker instalado:

### Paso 1: Construir imagen
```bash
docker build -t dashboard-auditorias .
```

### Paso 2: Ejecutar contenedor
```bash
docker run -p 8501:8501 dashboard-auditorias
```

### O usar Docker Compose:
```bash
docker-compose up -d
```

Acceder a http://localhost:8501

---

## 🧪 Verificar Instalación

### Verificar que todo está funcionando:

```bash
# Verificar Python
python -m pip list

# Debe mostrar:
# - pandas
# - streamlit
# - flask
# - openpyxl
# - numpy
```

### Probar Streamlit:
```bash
streamlit hello
```
Debe abrir una página con ejemplos de Streamlit.

---

## 🔧 Solución de Problemas Comunes

### Error: "Python no encontrado"
- **Solución**: Reinstalar Python desde https://www.python.org/
- Marcar "Add Python to PATH" durante la instalación

### Error: "modulenotfound: pandas"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error: "Puerto 8501 en uso"
- Streamlit está ya ejecutándose
- Detener el proceso anterior (Ctrl+C)
- O cambiar puerto: `streamlit run streamlit_app.py --server.port 8502`

### Error: "Excel file not found"
- Verificar que `CONTROL DE AUDITORIAS.xlsx` está en la carpeta principal
- No mover o renombrar el archivo

### Streamlit muy lento
- Limpiar caché: `streamlit cache clear`
- Cerrar navegadores innecesarios
- Usar `@st.cache_data` (ya implementado)

---

## 📋 Estructura de carpetas esperada

```
REPORTE DE CALIDAD/
│
├── app.py                           ← Flask app
├── streamlit_app.py                 ← Streamlit app (principal)
├── requirements.txt                 ← Dependencias
├── README.md                        ← Documentación
├── INSTALLATION.md                  ← Este archivo
├── DEPLOYMENT_GUIDE.md              ← Guía de despliegue
│
├── install.bat                      ← Script de instalación
├── run_streamlit.bat                ← Script para ejecutar Streamlit
├── run_flask.bat                    ← Script para ejecutar Flask
│
├── Dockerfile                       ← Para Docker
├── docker-compose.yml               ← Para Docker Compose
├── .gitignore                       ← Para Git
│
├── CONTROL DE AUDITORIAS.xlsx       ← Datos (IMPORTANTE)
│
├── .streamlit/
│   ├── config.toml                  ← Configuración Streamlit
│   └── secrets.example.toml         ← Ejemplo de secretos
│
├── .github/
│   └── workflows/
│       └── python-app.yml           ← GitHub Actions
│
├── templates/
│   └── dashboard.html               ← Página Flask
│
└── .venv/                           ← Entorno virtual (creado automáticamente)
```

---

## 🚀 Primeros pasos tras instalar

1. **Abre la aplicación** en tu navegador
2. **Revisa las pestañas**:
   - 📋 Auditorías: Ver datos principales
   - 🎯 Couching: Indicadores especializados
   - 📈 Desempeño: Puntajes de agentes
   - 🔍 Análisis: Filtros por criterio
   - 📚 Leyenda: Descripción de métricas

3. **Prueba descargando datos** en formato CSV

4. **Filtra por criterio** en la pestaña de análisis

---

## 💾 Actualizar datos

Si cambias el Excel:
1. Sólo refresca la página del navegador
2. Los datos se cargan automáticamente
3. No necesitas reiniciar la aplicación

---

## ❓ ¿Algo no funciona?

1. **Intenta actualizar todo:**
   ```bash
   pip install --upgrade streamlit flask pandas openpyxl
   ```

2. **Limpia caché:**
   ```bash
   streamlit cache clear
   ```

3. **Recrea el entorno:**
   ```bash
   rmdir /s .venv  (Windows)
   rm -rf .venv    (Mac/Linux)
   
   python -m venv .venv
   source .venv/bin/activate  (Mac/Linux)
   .venv\Scripts\activate.bat  (Windows)
   
   pip install -r requirements.txt
   ```

---

## 📞 Soporte

Si tienes dudas específicas sobre:
- **Streamlit**: https://docs.streamlit.io
- **Flask**: https://flask.palletsprojects.com
- **Python**: https://docs.python.org

---

**¡Listo para usar!** 🎉
Ahora puedes compartir la URL con tu equipo.
