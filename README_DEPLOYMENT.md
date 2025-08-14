# 🚀 Guía de Despliegue - Dashboard Dorada Control

## 📋 Requisitos Previos

- Python 3.12+
- PostgreSQL 16+
- Git

## 🐳 Despliegue con Docker (Recomendado)

### 1. Despliegue Local con Docker Compose

```bash
# Clonar el repositorio
git clone <repository-url>
cd dorada-control-bs

# Ejecutar con Docker Compose
docker-compose up --build

# El dashboard estará disponible en: http://localhost:8501
```

### 2. Despliegue con Docker

```bash
# Construir la imagen
docker build -t dorada-dashboard .

# Ejecutar el contenedor
docker run -p 8501:8501 \
  -e DB_HOST=your-db-host \
  -e DB_PORT=5432 \
  -e DB_NAME=dorada_dashboard \
  -e DB_USER=your-db-user \
  -e DB_PASSWORD=your-db-password \
  dorada-dashboard
```

## ☁️ Despliegue en la Nube

### Heroku

1. **Crear aplicación en Heroku:**
```bash
heroku create dorada-dashboard
```

2. **Configurar variables de entorno:**
```bash
heroku config:set DB_HOST=your-db-host
heroku config:set DB_PORT=5432
heroku config:set DB_NAME=dorada_dashboard
heroku config:set DB_USER=your-db-user
heroku config:set DB_PASSWORD=your-db-password
```

3. **Desplegar:**
```bash
git push heroku main
```

### Railway

1. **Conectar repositorio a Railway**
2. **Configurar variables de entorno en el dashboard de Railway**
3. **El despliegue será automático**

### Render

1. **Crear nuevo Web Service en Render**
2. **Conectar el repositorio de GitHub**
3. **Configurar:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0`
4. **Configurar variables de entorno**

## 🔧 Configuración de Base de Datos

### PostgreSQL Local

```bash
# Instalar PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres createdb dorada_dashboard

# Crear usuario (opcional)
sudo -u postgres createuser --interactive
```

### PostgreSQL en la Nube

#### Heroku Postgres
```bash
heroku addons:create heroku-postgresql:mini
```

#### Railway Postgres
- Crear servicio PostgreSQL en Railway
- Copiar las credenciales de conexión

#### Render Postgres
- Crear servicio PostgreSQL en Render
- Configurar las variables de entorno

## 🌐 Variables de Entorno

Configurar las siguientes variables de entorno:

```bash
DB_HOST=localhost          # Host de la base de datos
DB_PORT=5432              # Puerto de la base de datos
DB_NAME=dorada_dashboard  # Nombre de la base de datos
DB_USER=postgres          # Usuario de la base de datos
DB_PASSWORD=your-password # Contraseña de la base de datos
```

## 📊 Datos de Prueba

El sistema incluye datos de muestra con avances positivos para demostración:

- **15 indicadores de cumplimiento** con promedio del 86.4%
- **15 conceptos financieros** con promedio de ejecución del 86.4%
- **Filtros por:** Secretaría, Dependencia, Sector, Programa, Indicador

## 🔍 Solución de Problemas

### Error: "No start command could be found"
- Verificar que existe el archivo `Procfile` o `nixpacks.toml`
- Asegurar que el comando de inicio esté correctamente configurado

### Error de conexión a base de datos
- Verificar que las variables de entorno estén configuradas
- Confirmar que la base de datos esté accesible desde el servidor

### Error de dependencias
- Verificar que `requirements.txt` esté actualizado
- Revisar los logs de build para errores específicos

## 📞 Soporte

Para problemas de despliegue:
1. Revisar los logs de la aplicación
2. Verificar la configuración de la base de datos
3. Contactar al equipo de desarrollo

## 🎯 Características del Dashboard

- ✅ **Paleta de colores oficial de La Dorada** (rojo predominante)
- ✅ **Filtros avanzados** por dependencia, secretaría, programa, indicador
- ✅ **Datos reales con avances positivos**
- ✅ **Gráficos interactivos** con texto negro para mejor legibilidad
- ✅ **Responsive design** para diferentes dispositivos
- ✅ **Métricas en tiempo real** de cumplimiento y ejecución 