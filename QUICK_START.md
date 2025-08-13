# 🚀 Inicio Rápido - Dashboard Dorada Control

## Instalación Automática (Recomendado)

```bash
# 1. Dar permisos de ejecución al script de instalación
chmod +x install.sh

# 2. Ejecutar instalación automática
./install.sh
```

## Instalación Manual

### 1. Instalar dependencias
```bash
pip3 install -r requirements.txt
```

### 2. Configurar PostgreSQL
```bash
# Crear base de datos
sudo -u postgres createdb dorada_dashboard

# Configurar credenciales
cp config_example.py config.py
# Editar config.py con tus credenciales
```

### 3. Configurar base de datos
```bash
python3 setup_database.py
```

### 4. Procesar datos Excel
```bash
python3 data_processor.py
```

### 5. Ejecutar dashboard
```bash
streamlit run dashboard.py
```

## Uso Rápido

### Ejecutar dashboard:
```bash
./run_dashboard.sh
```

### Acceder al dashboard:
Abrir navegador en: http://localhost:8501

## Estructura de Archivos

```
dorada-control-bs/
├── 📊 dashboard.py              # Dashboard principal
├── 🔧 data_processor.py         # Procesa datos Excel
├── 📁 data_loader.py           # Carga archivos Excel
├── 🗄️  database.py              # Gestión PostgreSQL
├── ⚙️  config.py                # Configuración
├── 📋 requirements.txt          # Dependencias
├── 🚀 install.sh               # Instalación automática
├── ▶️  run_dashboard.sh         # Ejecutar dashboard
├── 📖 README.md                # Documentación completa
├── ⚡ QUICK_START.md           # Esta guía
└── 📄 Excel files...           # Tus archivos Excel
```

## Solución de Problemas Rápidos

### Error de conexión a PostgreSQL:
```bash
# Verificar que PostgreSQL esté ejecutándose
sudo systemctl status postgresql

# Iniciar si no está ejecutándose
sudo systemctl start postgresql
```

### Error de dependencias:
```bash
# Reinstalar dependencias
pip3 install --upgrade -r requirements.txt
```

### Error de permisos:
```bash
# Dar permisos de ejecución
chmod +x *.sh
```

## Comandos Útiles

```bash
# Verificar estado de la base de datos
python3 setup_database.py

# Reprocesar datos Excel
python3 data_processor.py

# Ejecutar dashboard en modo debug
streamlit run dashboard.py --logger.level debug
```

## Soporte

- 📖 Documentación completa: `README.md`
- 🐛 Reportar problemas: Crear issue en el repositorio
- 💬 Soporte: Contactar al equipo de desarrollo 