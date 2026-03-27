FROM python:3.11-slim

WORKDIR /app

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la aplicación
COPY . .

# Exponer puerto de Streamlit
EXPOSE 8501

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 streamlit_user && chown -R streamlit_user:streamlit_user /app
USER streamlit_user

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
