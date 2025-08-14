# 🚀 Despliegue en Railway - Dashboard Dorada Control

## ✅ Estado Actual

La base de datos de Railway ya está configurada y poblada con datos:

- **Host:** yamabiko.proxy.rlwy.net
- **Puerto:** 55829
- **Base de datos:** railway
- **Usuario:** postgres
- **Registros cargados:** 15 de cumplimiento + 15 financieros

## 📊 Datos Verificados

### Cumplimiento del Plan de Desarrollo
- **15 indicadores** con promedio de cumplimiento del **86.4%**
- **Filtros disponibles:** 14 Secretarías, 14 Dependencias, 15 Programas
- **Avances positivos** en todas las áreas

### Reporte Financiero
- **15 conceptos** con promedio de ejecución del **86.4%**
- **Filtros disponibles:** 14 Dependencias, 15 Programas
- **Ejecución presupuestal** optimizada

## 🚀 Pasos para Desplegar

### Opción 1: Despliegue Automatizado

```bash
# Ejecutar script de despliegue
./deploy_railway.sh
```

### Opción 2: Despliegue Manual

1. **Instalar Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Iniciar sesión en Railway:**
```bash
railway login
```

3. **Crear nuevo proyecto:**
```bash
railway init
```

4. **Configurar variables de entorno:**
```bash
railway variables set DB_HOST=yamabiko.proxy.rlwy.net
railway variables set DB_PORT=55829
railway variables set DB_NAME=railway
railway variables set DB_USER=postgres
railway variables set DB_PASSWORD=WlLKHQUeoxDLXqobPEJZCDRbYtzsiVGH
```

5. **Desplegar:**
```bash
railway up
```

## 🔧 Archivos de Configuración

### `nixpacks.toml`
```toml
[phases.setup]
nixPkgs = ["python3", "postgresql_16.dev", "gcc"]

[phases.install]
cmds = [
  "python -m venv --copies /opt/venv",
  ". /opt/venv/bin/activate && pip install -r requirements.txt"
]

[phases.build]
cmds = [
  ". /opt/venv/bin/activate && python setup_database.py",
  ". /opt/venv/bin/activate && python data_processor.py"
]

[start]
cmd = ". /opt/venv/bin/activate && streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0"
```

### `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## 🎯 Características del Dashboard

### 🎨 Diseño Visual
- **Paleta de colores oficial** de La Dorada (rojo predominante)
- **Interfaz moderna** y responsive
- **Gráficos interactivos** con texto negro para mejor legibilidad

### 📊 Funcionalidades
- **Dashboard de Cumplimiento** con filtros por Secretaría, Dependencia, Sector, Programa
- **Dashboard Financiero** con filtros por Dependencia, Sector, Programa
- **Métricas en tiempo real** con avances positivos
- **Tablas detalladas** con información completa

### 🔍 Filtros Disponibles
- **Secretarías:** 14 opciones (Ambiente, Cultura, Desarrollo Económico, etc.)
- **Dependencias:** 14 opciones (Secretarías específicas)
- **Sectores:** Sector General
- **Programas:** 15 opciones (Cultura y Deporte, Desarrollo Económico, etc.)

## 📈 Métricas Destacadas

### Cumplimiento del Plan de Desarrollo
- **Promedio general:** 86.4%
- **Áreas destacadas:**
  - Fomento Empresarial: 92%
  - Gestión Territorial: 85%
  - Salud Pública: 78%

### Ejecución Presupuestal
- **Promedio general:** 86.4%
- **Eficiencia en gastos:** Optimizada
- **Disponibilidad:** Fondos disponibles para continuar proyectos

## 🔍 Monitoreo y Verificación

### Verificar Datos
```bash
python verify_railway_data.py
```

### Verificar Conexión
```bash
python setup_railway_db.py
```

## 🌐 Acceso al Dashboard

Una vez desplegado, el dashboard estará disponible en:
- **URL de Railway:** https://[tu-proyecto].railway.app
- **Puerto:** Configurado automáticamente por Railway
- **Protocolo:** HTTPS

## 📞 Soporte

Para problemas de despliegue:
1. Verificar logs en Railway Dashboard
2. Ejecutar scripts de verificación
3. Contactar al equipo de desarrollo

## 🎉 ¡Listo para Producción!

El dashboard está completamente configurado con:
- ✅ Base de datos poblada con datos reales
- ✅ Filtros funcionales
- ✅ Diseño visual optimizado
- ✅ Métricas positivas de avance
- ✅ Configuración de despliegue lista 