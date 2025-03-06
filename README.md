# 🏫 AulaTrack - Sistema de Gestión de Reservas de Salas

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Django](https://img.shields.io/badge/Django-5.1-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blueviolet)
![License](https://img.shields.io/badge/License-MIT-yellow)

Plataforma web para la gestión inteligente de reservas de salas en instituciones educativas.

## 🖥️ Capturas de Pantalla
![Dashboard](https://via.placeholder.com/800x400.png?text=Dashboard+Interactivo)
![Formulario Reserva](https://via.placeholder.com/800x400.png?text=Formulario+de+Reserva)

## ✨ Características Principales
- 📅 Reservas en tiempo real con validación de horarios
- 👥 Gestión de usuarios y permisos multirol
- 🕒 Sistema de bloques horarios configurables
- 📊 Dashboard interactivo con estado actual de salas
- 🔑 Generación automática de claves de acceso
- 📱 Diseño responsive compatible con móviles
- 🚨 Validación de RUT chileno integrada

## 🛠️ Requisitos Técnicos
- Python 3.12+
- PostgreSQL 15+
- Django 5.1+
- Bootstrap 5.3+

## ⚙️ Instalación
```bash
# Clonar repositorio
git clone https://github.com/cy5k0/AulaTrack.git
cd AulaTrack

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar migraciones
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

## 📋 Configuración Inicial
1. Crear superusuario:
```bash
python manage.py createsuperuser
```
2. Acceder al panel de administración en `/admin`
3. Configurar salas y usuarios iniciales

## 🚀 Uso Básico
1. **Acceso al Dashboard**
   - URL: `http://localhost:8000/dashboard/`
   - Visualiza el estado actual de todas las salas

2. **Reserva de Salas**
   - Selecciona una sala disponible
   - Elige fecha y bloque horario
   - Completa los datos requeridos
   - Recibe tu clave de acceso única

3. **Gestión Administrativa**
   - Creación/Edición de usuarios
   - Configuración de salas
   - Monitoreo de reservas activas

## 🧩 Tecnologías Utilizadas
- **Backend:** Django, Django REST Framework
- **Frontend:** Bootstrap 5, JavaScript Vanilla
- **Base de Datos:** PostgreSQL
- **Autenticación:** Sistema personalizado con RUT
- **Despliegue:** Docker (próximamente)

## 🤝 Contribución
¡Tu ayuda es bienvenida! Sigue estos pasos:
1. Haz fork del proyecto
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y commitea: `git commit -m 'Add some feature'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia
Distribuido bajo licencia MIT. Ver `LICENSE` para más detalles.


---

Hecho con ❤️ para la educación chilena 🦅
