# 📊 Dashboard Dorada Control

Dashboard interactivo para visualizar información de cumplimiento del plan de desarrollo y reportes financieros de Dorada.

## 🚀 Características

- **Visualización Interactiva**: Gráficos dinámicos con Plotly
- **Base de Datos PostgreSQL**: Almacenamiento robusto de datos
- **Filtros Avanzados**: Búsqueda y filtrado de información
- **Métricas en Tiempo Real**: Indicadores clave de rendimiento
- **Interfaz Moderna**: Diseño responsive con Streamlit

## 📋 Requisitos

- Python 3.8+
- PostgreSQL
- pip

## 🛠️ Instalación

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd dorada-control-bs
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos PostgreSQL**:
   - Crear una base de datos llamada `dorada_dashboard`
   - Configurar las credenciales en `config.py` o crear un archivo `.env`

4. **Configurar variables de entorno** (opcional):
```bash
# Crear archivo .env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dorada_dashboard
DB_USER=postgres
DB_PASSWORD=tu_password
```

## 📊 Uso

### 1. Cargar datos a la base de datos

```bash
python data_processor.py
```

Este script:
- Lee los archivos Excel
- Procesa y limpia los datos
- Crea las tablas en PostgreSQL
- Inserta los datos en la base de datos

### 2. Ejecutar el dashboard

```bash
streamlit run dashboard.py
```

El dashboard estará disponible en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
dorada-control-bs/
├── dashboard.py              # Aplicación principal del dashboard
├── data_processor.py         # Script para procesar datos Excel
├── data_loader.py           # Cargador de datos Excel
├── database.py              # Gestión de base de datos PostgreSQL
├── config.py                # Configuración de la aplicación
├── requirements.txt         # Dependencias de Python
├── README.md               # Este archivo
├── % Cumplimiento 2025 Plan de Desarrollo.xlsx
└── Reporte financiero 30 de junio 2025.xlsx
```

## 📈 Funcionalidades del Dashboard

### Cumplimiento Plan de Desarrollo
- **Métricas Clave**: Promedio de cumplimiento, total de indicadores
- **Gráficos**: Distribución de cumplimiento, top 10 indicadores
- **Filtros**: Por porcentaje mínimo y búsqueda de indicadores
- **Tabla Detallada**: Vista completa de todos los indicadores

### Reporte Financiero
- **Métricas Clave**: Presupuesto total, ejecutado, disponible
- **Gráficos**: Distribución presupuestaria, ejecución vs presupuesto
- **Análisis**: Porcentaje de ejecución, top ejecutores
- **Filtros**: Por porcentaje de ejecución y búsqueda de conceptos

## 🔧 Configuración de Base de Datos

### Crear base de datos PostgreSQL:

```sql
CREATE DATABASE dorada_dashboard;
```

### Tablas creadas automáticamente:

**cumplimiento_plan_desarrollo**:
- `id`: Identificador único
- `indicador`: Nombre del indicador
- `meta_anual`: Meta anual
- `avance_actual`: Avance actual
- `porcentaje_cumplimiento`: Porcentaje de cumplimiento
- `fecha_actualizacion`: Fecha de actualización
- `created_at`: Timestamp de creación

**reporte_financiero**:
- `id`: Identificador único
- `concepto`: Concepto financiero
- `presupuesto_anual`: Presupuesto anual
- `ejecutado`: Monto ejecutado
- `disponible`: Monto disponible
- `porcentaje_ejecucion`: Porcentaje de ejecución
- `fecha_reporte`: Fecha del reporte
- `created_at`: Timestamp de creación

## 🎨 Personalización

### Modificar estilos CSS:
Editar la sección de CSS en `dashboard.py` para cambiar colores, fuentes y layout.

### Agregar nuevas visualizaciones:
1. Crear nuevas funciones en `dashboard.py`
2. Agregar los gráficos usando Plotly
3. Integrar con los datos de la base de datos

### Extender funcionalidades:
- Agregar exportación de datos
- Implementar alertas automáticas
- Conectar con APIs externas
- Agregar autenticación de usuarios

## 🐛 Solución de Problemas

### Error de conexión a base de datos:
1. Verificar que PostgreSQL esté ejecutándose
2. Confirmar credenciales en `config.py`
3. Verificar que la base de datos exista

### Error al cargar archivos Excel:
1. Verificar que los archivos estén en el directorio correcto
2. Confirmar que los archivos no estén corruptos
3. Verificar permisos de lectura

### Dashboard no se carga:
1. Verificar que Streamlit esté instalado
2. Confirmar que todas las dependencias estén instaladas
3. Revisar logs de error en la consola

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas, contactar al equipo de desarrollo. 