# Proyecto de Análisis Financiero y Recomendación de Inversiones de Empresas Energéticas


### Este proyecto tiene como objetivo proporcionar una solución integral para los analistas e inversionistas especializados en el sector energético, facilitando el acceso a datos actualizados de cotizaciones diarias de empresas que cotizan en bolsas internacionales. Mediante la integración de tecnologías avanzadas, se automatiza la extracción, almacenamiento y análisis de estos datos.

## Descripción del Proyecto

### Nuestro sistema se encarga de extraer diariamente datos financieros actualizados de empresas energéticas desde Yahoo Finance, procesarlos mediante un pipeline automatizado de ETL, y almacenarlos en un data warehouse en Amazon Redshift. A partir de estos datos, se realizan análisis exploratorios (EDA), predicciones con modelos de machine learning y visualizaciones interactivas, con el fin de generar recomendaciones de inversión para nuestros usuarios.

### Problema

Los analistas e inversionistas en el sector energético enfrentan dificultades para obtener datos financieros actualizados y confiables sobre las empresas energéticas que cotizan en bolsas internacionales. Esta falta de datos actualizados puede dificultar la toma de decisiones informadas sobre inversiones y estrategias de mercado.

### Solución

La solución planteada consiste en un sistema automatizado que extrae diariamente los datos financieros de empresas energéticas de [Yahoo Finance](https://finance.yahoo.com "Yahoo Finance") utilizando web scraping. Los datos extraídos se almacenan en un data warehouse en Amazon Redshift, y las cotizaciones históricas y actuales se visualizan en dashboards interactivos creados con Power BI. Adicionalmente, implementamos modelos de machine learning que predicen el comportamiento futuro de las acciones, ayudando a los analistas a tomar decisiones informadas.

### Características Principales

- Extracción de datos financieros mediante web scraping.

- Automatización de procesos ETL usando Airflow en Composer de Google.

- Análisis exploratorio de datos (EDA) para obtener insights iniciales.

- Análisis avanzado de datos financieros.

- Modelo de recomendación de inversión basado en deep learning.

- Visualización interactiva de los datos financieros históricos y actuales mediante Power BI.

- Despliegue del modelo de machine learning para predicción de comportamientos futuros en las bolsas internacionales.

### Tecnologías Utilizadas

**Docker:** Contenerización y gestión de entornos de desarrollo.

**Airflow y Composer de Google:** Orquestación del pipeline de ETL.

**Amazon Redshift:** Almacenamiento de datos en un data warehouse escalable.

**Python:** Lenguaje principal para la automatización de procesos y análisis de datos.

**Streamlit:** Visualización y despliegue de aplicaciones interactivas de machine learning.

**Power BI:** Herramienta de visualización de datos para la creación de dashboards interactivos.

**PostgreSQL:** Sistema de gestión de bases de datos utilizado para la extracción y análisis de los datos financieros.

### Datos Financieros

Los datos extraídos de Yahoo Finance para cada empresa energética incluyen las siguientes columnas:

- **Date**

- **Open**

- **High**

- **Low**

- **Close**

- **Volume**

- **Dividends**

- **Stock Split**

### Metodología de Gestión de Proyectos

Para la gestión del proyecto, implementamos la metodología Scrum, organizando las fases del proyecto en cuatro sprints semanales. Inicialmente utilizamos Trello como herramienta de gestión, pero luego migramos a Jira para un seguimiento más detallado de las tareas.

## Estructura del Equipo
- **José Paternina Orozco** - Team Leader

    [Linkedin](https://www.linkedin.com/in/josepaterninaorozco/?originalSubdomain=co)

    [Gmail](mailto:juanantonio.r.m94@gmail.com)

- **Juan Cortez Zamar** - Project Manager & Data Engineer

    [Linkedin](https://www.linkedin.com/in/juanzamar)

    [Github](https://github.com/juancorzamar93)

    [Gmail](mailto:juancorzamar@gmail.com)
- **Nicolas Salamanca** - Data Engineer
  
  [Linkedin](https://www.example.com/image.jpg)

  [Github](https://github.com/NICOLAS-ANTONIO)

  [Gmail](mailto:nicolas.antonio.sm@outlook.com)

- **Juan Antonio Reyes Mendoza** - Data Scientist
 
  [Linkedin](https://www.linkedin.com/in/juan-antonio-reyes-mendoza/)

  [Github](https://github.com/JuanAntonioRe)

  [Gmail](mailto:juanantonio.r.m94@gmail.com)
  
- **Laura Minaya** - Business Intelligence Analyst
  
  [Linkedin](https://www.linkedin.com/in/laura-m-3a878b212/)

  [Gmail](mailto:lauminagui@gmail.com)

### Despliegue del Producto
Este proyecto está siendo desarrollado como parte de un programa de aceleramiento en No Country, el cual tiene como objetivo principal aprender y reforzar habilidades de trabajo en equipo, así como el desarrollo y uso de tecnologías en el campo de Data BI. Aunque no es un producto comercializable en esta etapa, el enfoque está en la mejora continua de habilidades técnicas y colaborativas.

