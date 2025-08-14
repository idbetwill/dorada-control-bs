# 🔗 Conexión del Proyecto con Railway

## ✅ Estado Actual

Tu proyecto ya está desplegado en Railway y tienes una base de datos PostgreSQL configurada. Ahora necesitas conectar ambos servicios.

## 🚀 Pasos para Conectar

### 1. **Verificar Variables de Entorno en Railway**

En el dashboard de Railway, ve a tu servicio **Postgres-C-Jt** y en la pestaña **"Variables"** verás estas variables automáticas:

```
PGHOST=*******
PGPORT=*******
PGDATABASE=*******
PGUSER=*******
PGPASSWORD=*******
DATABASE_URL=*******
```

### 2. **Configurar Variables en el Proyecto**

En tu servicio **dorada-control-bs**, ve a la pestaña **"Variables"** y agrega estas variables:

```bash
# Copia los valores desde Postgres-C-Jt
PGHOST=[valor desde Postgres-C-Jt]
PGPORT=[valor desde Postgres-C-Jt]
PGDATABASE=[valor desde Postgres-C-Jt]
PGUSER=[valor desde Postgres-C-Jt]
PGPASSWORD=[valor desde Postgres-C-Jt]
DATABASE_URL=[valor desde Postgres-C-Jt]
```

### 3. **Conectar los Servicios**

En Railway, puedes conectar los servicios automáticamente:

1. Ve a tu servicio **dorada-control-bs**
2. En la pestaña **"Variables"**
3. Haz clic en **"+ New"**
4. Selecciona **"Variable Reference"**
5. Selecciona el servicio **Postgres-C-Jt**
6. Selecciona las variables que necesitas

### 4. **Verificar la Conexión**

Ejecuta este comando para verificar que la conexión funcione:

```bash
python connect_railway_db.py
```

## 🔧 Configuración Automática

El archivo `config.py` ya está configurado para usar las variables de Railway automáticamente:

```python
DB_CONFIG = {
    'host': os.getenv('PGHOST', os.getenv('DB_HOST', 'localhost')),
    'port': os.getenv('PGPORT', os.getenv('DB_PORT', '5432')),
    'database': os.getenv('PGDATABASE', os.getenv('DB_NAME', 'railway')),
    'user': os.getenv('PGUSER', os.getenv('DB_USER', 'postgres')),
    'password': os.getenv('PGPASSWORD', os.getenv('DB_PASSWORD', 'postgres'))
}
```

## 📋 Variables Necesarias

### Variables Principales (Railway las proporciona automáticamente)
- `PGHOST` - Host de la base de datos
- `PGPORT` - Puerto de la base de datos
- `PGDATABASE` - Nombre de la base de datos
- `PGUSER` - Usuario de la base de datos
- `PGPASSWORD` - Contraseña de la base de datos
- `DATABASE_URL` - URL completa de conexión

### Variables Opcionales (para compatibilidad)
- `DB_HOST` - Host alternativo
- `DB_PORT` - Puerto alternativo
- `DB_NAME` - Nombre alternativo
- `DB_USER` - Usuario alternativo
- `DB_PASSWORD` - Contraseña alternativa

## 🎯 Pasos Rápidos

### Opción 1: Usando Railway CLI

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Iniciar sesión
railway login

# Conectar al proyecto
railway link

# Ver variables disponibles
railway variables

# Configurar variables automáticamente
railway variables set PGHOST=$(railway variables get PGHOST --service Postgres-C-Jt)
railway variables set PGPORT=$(railway variables get PGPORT --service Postgres-C-Jt)
railway variables set PGDATABASE=$(railway variables get PGDATABASE --service Postgres-C-Jt)
railway variables set PGUSER=$(railway variables get PGUSER --service Postgres-C-Jt)
railway variables set PGPASSWORD=$(railway variables get PGPASSWORD --service Postgres-C-Jt)
```

### Opción 2: Manual desde Dashboard

1. **Copiar variables desde Postgres-C-Jt**
2. **Pegar en dorada-control-bs**
3. **Reiniciar el servicio**

## 🔍 Verificación

### Script de Verificación
```bash
python connect_railway_db.py
```

### Verificación Manual
```bash
# Conectar a la base de datos
PGPASSWORD=[tu_password] psql -h [tu_host] -U [tu_user] -d [tu_database] -p [tu_puerto]

# Verificar tablas
\dt

# Verificar datos
SELECT COUNT(*) FROM cumplimiento_plan_desarrollo;
SELECT COUNT(*) FROM reporte_financiero;
```

## 🚨 Solución de Problemas

### Error: "No se detectaron variables de Railway"
- Verificar que el proyecto esté desplegado en Railway
- Verificar que las variables estén configuradas
- Revisar los logs del servicio

### Error: "Connection refused"
- Verificar que el servicio PostgreSQL esté activo
- Verificar que las credenciales sean correctas
- Verificar que el puerto esté abierto

### Error: "Database does not exist"
- Verificar que la base de datos esté creada
- Ejecutar `python setup_railway_db.py` para crear las tablas

## 📞 Soporte

Si tienes problemas:

1. **Revisar logs:** Railway Dashboard → Servicio → Logs
2. **Verificar variables:** Railway Dashboard → Servicio → Variables
3. **Reiniciar servicio:** Railway Dashboard → Servicio → Settings → Restart
4. **Contactar soporte:** Si el problema persiste

## 🎉 ¡Listo!

Una vez configurado, tu dashboard estará conectado a la base de datos de Railway y podrás:

- ✅ Ver datos en tiempo real
- ✅ Usar filtros funcionales
- ✅ Acceder desde cualquier lugar
- ✅ Escalar automáticamente 