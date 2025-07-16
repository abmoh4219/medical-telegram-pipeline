# Medical Telegram Pipeline

## Overview

This repository contains the code and data pipeline for the **"Shipping a Data Product: From Raw Telegram Data to an Analytical API"** project. The goal is to scrape medical-related Telegram channels, transform the data into an analytical format, and enrich it for insights.

## Project Structure

- **.env**: Stores sensitive credentials (gitignored).
- **.gitignore**: Excludes virtual environment, sensitive files, and large generated data.
- **requirements.txt**: Lists Python dependencies (e.g., dbt-postgres).
- **docker-compose.yml**: Configures the PostgreSQL database via Docker.
- **data/raw/**: Contains scraped CSV files and images from Telegram channels.
- **data/processed/**: Reserved for processed/enriched data (currently empty).
- **src/**: Houses the scraping script (`scrape_telegram.py`) and future enrichment scripts.
- **dbt_project/medical_telegram_pipeline/**: Contains dbt configuration and models for data transformation.

## Setup Instructions

1. **Install Dependencies:**
   - Create a virtual environment:  
     `python -m venv venv`
   - Activate it:  
     `.\venv\Scripts\Activate.ps1` (PowerShell)
   - Install requirements:  
     `pip install -r requirements.txt`

2. **Start PostgreSQL:**
   - Run `docker-compose up -d` to start the database.

3. **Run the Pipeline:**
   - Execute `python src/scrape_telegram.py` to scrape data (requires Telegram API credentials).
   - Use dbt commands (e.g., `dbt run`) from `dbt_project/medical_telegram_pipeline/` to transform data.

## Progress

- **Task 0**: Project setup completed with Docker and virtual environment.
- **Task 1**: Scraped 276 messages from 3 channels, stored in `data/raw/` and `raw_messages` table.
- **Task 2**: Transformed data into a star schema using dbt, with models for channels, dates, and messages. Documentation generated.

## Upcoming Work

- **Task 3**: Enrich data with object detection using YOLO on images.
- **Future**: Develop an API for analytical access.

## Notes

- The `target/` folder in `dbt_project/medical_telegram_pipeline/` is gitignored as it contains large, regeneratable files.
- Ensure `.env` is configured with
