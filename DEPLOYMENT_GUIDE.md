# 🚀 Guía de Despliegue en Streamlit Cloud

Esta guía te ayudará a compartir tu dashboard en Streamlit Cloud de forma fácil y gratuita.

## Paso 1: Preparar tu Repositorio en GitHub

### 1.1 Crear un repositorio en GitHub
```bash
# Inicializar git (si no está inicializado)
git init

# Agregar todos los archivos
git add .

# Commit inicial
git commit -m "Initial commit: Dashboard auditorías"

# Agregar remote origen
git remote add origin https://github.com/TU_USUARIO/dashboard-auditorias.git

# Push a GitHub
git push -u origin main
```

## Paso 2: Conectar con Streamlit Cloud

### 2.1 Crear cuenta en Streamlit Cloud
1. Ir a [streamlit.io/cloud](https://streamlit.io/cloud)
2. Hacer clic en "Sign up"
3. Conectar con tu cuenta de GitHub
4. Autorizar Streamlit Cloud

### 2.2 Crear nuevo app
1. Click en "Create app"
2. Seleccionar:
   - **Repository**: tu-usuario/dashboard-auditorias
   - **Branch**: main
   - **Main file path**: streamlit_app.py
3. Click en "Deploy"

## Paso 3: Compartir el Enlace

Una vez desplegado, obtendrás un enlace como:
```
https://dashboard-auditorias-TU_USUARIO.streamlit.app
```

Puedes compartir este enlace con tu equipo. No requiere instalación previa de Python.

---

## Alternativa: Despliegue Local con Docker

Si prefieres ejecutar localmente o en tu propio servidor:

### Instalación de Docker
```bash
# En Windows: Descargar Docker Desktop desde docker.com
# En Mac/Linux: brew install docker
```

### Ejecutar con Docker Compose
```bash
docker-compose up -d
```

La aplicación estará en `http://localhost:8501`

### Ejecutar con Docker directamente
```bash
docker build -t dashboard-auditorias .
docker run -p 8501:8501 dashboard-auditorias
```

---

## Estructura de Carpetas Recomendada

```
dashboard-auditorias/
├── app.py                           # Flask (opcional)
├── streamlit_app.py                 # Streamlit (principal)
├── requirements.txt                 # Dependencias
├── CONTROL DE AUDITORIAS.xlsx       # Data
├── README.md                        # Documentación
├── Dockerfile                       # Para Docker
├── docker-compose.yml               # Para Docker Compose
├── .gitignore
├── .streamlit/
│   └── config.toml                  # Configuración Streamlit
└── templates/
    └── dashboard.html               # HTML para Flask
```

---

## Variables de Entorno (Opcional)

Si necesitas variables de entorno, crea un archivo `.env.example`:

```bash
# .env.example
EXCEL_FILE=CONTROL DE AUDITORIAS.xlsx
DEBUG=false
```

En Streamlit Cloud, agregálas en Settings → Secrets.

---

## Troubleshooting

### Error: "streamlit: command not found"
```bash
pip install streamlit --upgrade
```

### Error: "Excel file not found"
- Verificar que el archivo `.xlsx` está en el repositorio
- Ajustar ruta en el código si es necesario

### Aplicación lenta
- Usar `@st.cache_data` para cachear datos (ya está implementado)
- Limitar gráficos complejos

---

## Mantenimiento

### Actualizar datos
1. Modificar archivo Excel localmente
2. `git add CONTROL DE AUDITORIAS.xlsx`
3. `git commit -m "Update data"`
4. `git push`
5. Streamlit redesplegará automáticamente

### Actualizar código
1. Modificar archivos `.py`
2. `git add .`
3. `git commit -m "Update features"`
4. `git push`
5. Streamlit redesplegará en segundos

---

## Tips de Seguridad

- No subir archivos con datos sensibles sin encriptar
- Usar `.gitignore` para excluir archivos locales
- En producción, considerar autenticación con Streamlit Cloud Pro
- Revisar permisos de acceso periódicamente

---

## Soporte y Recursos

- [Documentación Streamlit](https://docs.streamlit.io)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [GitHub Actions para CI/CD](https://github.com/features/actions)

---

**¡Listo!** Tu dashboard ahora es accesible desde cualquier navegador 🎉
