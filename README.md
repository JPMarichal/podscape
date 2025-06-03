# Generador de Posts para Podcast "Mis Lecturas sobre la Fe"

![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

Aplicación web para generar publicaciones de redes sociales a partir de episodios del podcast "Mis Lecturas sobre la Fe". La aplicación extrae información de los episodios y genera publicaciones formateadas listas para compartir en WhatsApp, Facebook y otras plataformas.

## 🚀 Características

- Extracción automática de información de episodios de podcast
- Generación de publicaciones formateadas para redes sociales
- Interfaz web intuitiva
- Soporte para múltiples formatos de salida
- Contenedor Docker para fácil despliegue

## 🛠️ Requisitos Previos

- Docker y Docker Compose instalados
- Git (opcional, para control de versiones)

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/podcast-post-generator.git
   cd podcast-post-generator
   ```

2. Copia el archivo de configuración de ejemplo y edítalo según sea necesario:
   ```bash
   cp .env.example .env
   ```

## 🐳 Uso con Docker (Recomendado)

1. Construye y ejecuta los contenedores:
   ```bash
   docker-compose up --build
   ```

2. Abre tu navegador y visita:
   ```
   http://localhost:8001
   ```

## 🏗️ Desarrollo Local

Si prefieres ejecutar el proyecto sin Docker:

1. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

## 🌐 Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Configuración de la aplicación
APP_NAME="Generador de Posts para Podcast"
DEBUG=True

# Configuración del feed del podcast
FEED_URL="https://www.spreaker.com/show/6622205/episodes/feed"
```

## 📂 Estructura del Proyecto

```
.
├── app/                    # Código fuente de la aplicación
│   ├── __init__.py
│   ├── main.py             # Punto de entrada de FastAPI
│   ├── feed_processing.py   # Procesamiento de feeds
│   ├── interfaces.py        # Interfaces y modelos
│   ├── social_media_formatters.py  # Formatos de publicaciones
│   └── templates/           # Plantillas HTML
│       └── index.html
├── tests/                  # Pruebas unitarias
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, lee nuestras [pautas de contribución](CONTRIBUTING.md) antes de enviar un pull request.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

## 📞 Contacto

Si tienes preguntas o sugerencias, no dudes en abrir un issue o contactar al equipo de desarrollo.

---

<div align="center">
  <p>Hecho con ❤️ para la comunidad de "Mis Lecturas sobre la Fe"</p>
  <p>✨ 2025 - Generador de Posts para Podcast</p>
</div>
