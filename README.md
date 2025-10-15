\#  Sistema de ingesta y análisis de datos para la optimización dinámica de precios



Este proyecto es un prototipo funcional de un sistema de ingeniería de datos que simula la optimización de precios para una empresa de retail. El sistema extrae precios de la competencia (suburbia), genera datos internos de ventas e inventario, y aplica un modelo de reglas para recomendar precios óptimos por producto.



---



\### Características Principales



\* \*\*Web Scraping Dinámico\*\*: Utiliza Selenium para extraer datos de productos y precios de sitios web en este caso, Suburbia México.

\* \*\*Generación de Datos Sintéticos\*\*: Crea un ecosistema de datos realista (ventas, inventario, catálogo) basado en los productos extraídos del scraping, ideal para este prototipo donde los datos reales son sensibles.

\* \*\*Pipeline de Datos ELT\*\*: Sigue un flujo de trabajo de ingeniería de datos donde los datos se extraen (Extract), se cargan (Load) y luego se transforman (Transform).

\* \*\*Modelo de Precios Basado en Reglas\*\*: Un modelo sencillo pero efectivo que recomienda precios basándose en factores clave como el precio de la competencia y los niveles de inventario.

\* \*\*Código modular y orquestado\*\*: El proyecto está estructurado en módulos claros (ingesta, procesamiento, modelo y cuenta con un orquestador (`main.py`) para ejecutar todo el flujo de forma automática.



---



\### Tecnologías Utilizadas



\* \*\*Lenguaje\*\*: Python 3.12

\* \*\*Web Scraping\*\*: Selenium y BeautifulSoup4

\* \*\*Manipulación de Datos\*\*: Pandas

\* \*\*Orquestación Conceptual\*\*: Preparado para ser adaptado a herramientas como Airflow.



---



\### Estructura del Proyecto





precios\_dinamicos/

│

├── data/              # Carpeta para los datos (crudos, procesados, etc.)

├── src/               # Código fuente.

│   ├── ingestion/     # Scripts para obtener datos (scraping, generación).

│   ├── processing/    # Scripts para limpiar y transformar datos.

│   ├── modeling/      # Scripts para el modelo de precios.

│   └── main.py        # El orquestador que ejecuta todo el pipeline.

│

├── requirements.txt   # Lista de librerías de Python necesarias.

└── README.md          # Guía de instalación y ejecución







\### Guía de Instalación y Ejecución





\*\*1. Clona el Repositorio\*\*

bash

git clone \[https://github.com/tu-usuario/precios\_dinamicos.git](https://github.com/tu-usuario/precios\_dinamicos.git)

cd precios\_dinamicos





\*\*2. Crea y Activa un Entorno Virtual\*\*

Es una buena práctica para no instalar las librerías en tu sistema global.

bash

\# Crear el entorno

python -m venv .venv



\# Activar en Windows

.venv\\Scripts\\activate



\# Activar en Mac/Linux

source .venv/bin/activate





\*\*3. Instala las Dependencias\*\*

bash

pip install -r requirements.txt





\*\*4. Ejecutar el Pipeline

Este es el único comando que necesitas para correr el pipeline compelto. Asegúrate de estar en la carpeta raíz del proyecto.

bash

python -m src.main



El script comenzará a ejecutar cada fase: primero el scraper, luego el generador, el transformador y finalmente el modelo, al terminar los resultados los encontraremos en la carpeta `data/recommendations/`.

