#!/bin/bash

# Activar el entorno virtual
source /home/jgfhvji/Desktop/c20-71-n-data-bi/bin/activate

# Navegar al directorio del proyecto
cd /home/jgfhvji/Desktop/c20-71-n-data-bi/web_scraping

# Ejecutar el script de Python
python3 historical_data_scraper.py

# Actualizar el repositorio Git
git add .
git commit -m "Actualización diaria de datos: $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main

# Desactivar el entorno virtual
deactivate
