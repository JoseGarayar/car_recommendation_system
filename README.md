# Django project - Used Cars Website

## Project Description

This project is a Django application designed to manage a used cars website. A video explaining the functionalities of the webpage can be found here:  [**Youtube video**](https://youtu.be/_pJhJk7SA8Y) 

Below are the main features and components developed:

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

5. Optional: Create new users

```bash
docker-compose -f local.yml run --rm django python manage.py create_new_users app_django/users/media/usuarios.csv
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

It is used to clear the variables in terms of structure, change data type and generate extra variables. It is mentioned that it is not preprocessing or modeling feature engineering.

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

### 02_app_modeling_01.ipynb - 02_app_modeling_02.ipynb

Process of searching for the best hyperparameters for the model. A base XGBoost Regressor is used.

The tuning process involves randomly generating a set of hyperparameters, tuning the seed to achieve the best partitioning into subsets, and finally fitting the model. These results are partially saved in a CSV file that is used to retrain the model and select, based on expert criteria, the set of parameters that maximizes the R², which is the target metric.

This notebook handles the initial modeling phase:

- Imports necessary libraries.
- Declares hyperparameters for model training.
- Creates a multisession manager.
- Declares input for multisession to handle multiple modeling tasks concurrently.

### 03_app_tuned_model.ipynb

The best set of hyperparameters is chosen based on expert judgment. The estimator is then retrained based on the record that meets the boundary conditions.

This notebook focuses on tuning the model:

- Imports necessary libraries and cleans the data.
- Finds the best model by tuning hyperparameters.
- Refits the model with the found hyperparameters.
- Reevaluates the model and displays the results.
- Identifies important features.
- Saves the categories and unique models per brand.
- Includes a test case.

### 04_app_calibration_process.ipynb

The base predictions of the estimator are both underestimating and overestimating the target. Therefore, it is necessary to move all of them to the calibration line.

This is done through another model known as a calibrator. It takes the predictions of the regressor with a driver, which is the vehicle's year. With this, the best hyperparameters are sought again using the same criteria as in the previous step.

This notebook covers the calibration process:

- Imports necessary libraries.
- Loads and cleans the dataframe.
- Reads the model and gets predictions.
- Plots a calibration curve.
- Starts the calibration by declaring hyperparameters.
- Creates a multisession manager and declares input for multisession.

### 05_app_tuned_calibrator.ipynb

In the same way as step 03, the parameters that maximize the R² of the calibrator are selected. This model receives two variables as input, and with this, the final predictions are obtained.

This notebook focuses on tuning the calibrator:

- Imports necessary libraries.
- Finds the best model for calibration.
- Refits the model with the found hyperparameters.
- Reevaluates the model and displays the results.
- Identifies important features.
- Saves the categories and unique models per brand.
- Includes a test case and plots a calibration curve.
