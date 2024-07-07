# Proyecto Django - Used Cars Website

## Project Description

This project is a Django application designed to manage a used cars sales website. Below are the main features and components developed:

### Features

1. Data Models and Database
    - Data models were developed to manage information about cars and users.
    - PostgreSQL was used as the database.
    - The entire environment is dockerized to facilitate deployment and setup.

2. Data Extraction via Web Scraping
    - Code was developed to extract data from websites like Autocosmos and Neoautos using web scraping techniques.
    - Extracted data is saved to CSV files for further processing.

3. Django Command for Data Import
    - A custom Django command was created to read the CSV files generated from web scraping and add the data to the PostgreSQL database.

4. Machine Learning Model
    - A machine learning model was developed to estimate the price of listed cars.
    - This model integrates with the database to provide accurate estimates based on stored data.

5. Responsive Frontend
    - A responsive frontend was designed for the website, ensuring an optimal user experience on both desktop and mobile devices.

6. Cold Start Recommendation System
    - The website features an integrated cold start recommendation system that suggests cars to users even when there is little information available about their preferences.

## Commands for Django App

1. To run project in local

```bash
docker-compose -f local.yml up --build
```

2. How to add cars to the DB using a command

```bash
docker-compose -f local.yml run --rm django python manage.py load_cars_from_csv app_model/datasets/clean/data.csv
```

3. Optional: To make migrations (not needed unless some changes in DB models has been applied)

```bash
docker-compose -f local.yml run --rm django python manage.py makemigrations
```

4. Optional: To create superuser (all privileges)

```bash
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```


## Proyecto de Web Scraping con Selenium y BeautifulSoup

Este proyecto utiliza `Selenium` y `BeautifulSoup` para realizar web scraping y análisis de datos con `pandas`. A continuación, se presentan las instrucciones para instalar los requisitos necesarios y ejecutar el proyecto.

### Requisitos

Para ejecutar este proyecto, necesitarás tener instaladas las siguientes bibliotecas de Python:

- `selenium`
- `beautifulsoup4`
- `pandas`
- `chromium-browser`

### Instalación

#### Instalar las dependencias
Instala las dependencias usando pip:

```bash
pip install -r requirements.txt
```

#### Instalar Chromium
Instala chromium-browser en tu sistema. Aquí se muestra cómo hacerlo en varias plataformas

En Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y chromium-browser
```

#### Modelamiento

Notebook 01: 01_app_preprocessing.ipynb

Se usa para limpiar las variables en terminos de estructura, cambiar tipo de datos y generar varibles extra.
Se menciona que no es el preprocessing ni el feature engineering de modelamiento

Notebook 02: 01_app_modeling_01.ipynb - 01_app_modeling_02.ipynb
Proceso de búsqueda de mejores hiperparámetros para el modelo. Se usa uno base de XGboost Regressor.

El tuning consiste es generar aleatoriamente un set de hiperparametros, tunear la semillar para realizar la mejor partición en subsets
y finalmente fitear el modelo. Estos resultados se guardan parcialemente en un csv que sirve para reentrenar el modelo y seleccionar
por criterio experto que set de parámetros maximiza el R2, el cual es lá metrica objetivo.

Notebook 03: 03_app_tuned_model.ipynb
Se escoge el mejor set de hiperparámetros en base a criterio experto. Luego se reentrena el estimador en base al registro que cumpla
las condiciones de borde

Notebook 04: 04_app_calibration_process.ipynb
Las predicciones base del estimador esta subestimando como sobrestimando el target, por tal motivo, se necesita mover todas ellas
a la línea de calibración. Esto se realiza a través de otro modelo conocido como calibrador, a el ingresa las predicciones del
regresor con un driver, el cual es el año del vehiculo, con esto se vuelve a buscar los mejores hiperparametros con el mismo
cruiterio del paso previo.

Notebook 05: 05_app_tuned_calibrator.ipynb
De la misma forma que el paso 03, se selecciona los parámetros que maximan el r2 del calibrador. Este recibe dos variables como
input y con esto se obtienen las predicciones finales.



