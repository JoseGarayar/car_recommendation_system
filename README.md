# Django project - Used Cars Website

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


## Web Scraping Project using Selenium and BeautifulSoup

This project uses `Selenium` and `BeautifulSoup` to perform web scraping and data analysis with `pandas`. Below are instructions to install the necessary requirements and run the project.

### Requirements

To run this project, you will need to have the following Python libraries installed:

- `selenium`
- `beautifulsoup4`
- `pandas`
- `chromium-browser`

### Installation

#### Install dependencies
Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

#### Install Chromium
Install chromium-browser on your system. Here's how to do it on various platforms

Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y chromium-browser
```

## Estimator model project

### 01_app_preprocessing.ipynb

This notebook focuses on data preprocessing steps for two datasets: Neoauto and Autocosmos.

Neoauto:

- Declares paths and constants.
- Cleans and validates numerical features.
- Cleans and validates categorical features (Brands, Models, Transmission, Version, Upholstery, Color, Location, Fuel_type).
- Performs feature engineering and saves the cleaned data to a CSV file.

Autocosmos:

- Reads data.
- Cleans and validates numerical and categorical features similar to Neoauto.
- Performs feature engineering and saves the cleaned data to a CSV file.

### 02_app_modeling_01.ipynb

This notebook handles the initial modeling phase:

- Imports necessary libraries.
- Declares hyperparameters for model training.
- Creates a multisession manager.
- Declares input for multisession to handle multiple modeling tasks concurrently.

### 03_app_tuned_model.ipynb

This notebook focuses on tuning the model:

- Imports necessary libraries and cleans the data.
- Finds the best model by tuning hyperparameters.
- Refits the model with the found hyperparameters.
- Reevaluates the model and displays the results.
- Identifies important features.
- Saves the categories and unique models per brand.
- Includes a test case.

### 04_app_calibration_process.ipynb

This notebook covers the calibration process:

- Imports necessary libraries.
- Loads and cleans the dataframe.
- Reads the model and gets predictions.
- Plots a calibration curve.
- Starts the calibration by declaring hyperparameters.
- Creates a multisession manager and declares input for multisession.

### 05_app_tuned_calibrator.ipynb

This notebook focuses on tuning the calibrator:

- Imports necessary libraries.
- Finds the best model for calibration.
- Refits the model with the found hyperparameters.
- Reevaluates the model and displays the results.
- Identifies important features.
- Saves the categories and unique models per brand.
- Includes a test case and plots a calibration curve.
