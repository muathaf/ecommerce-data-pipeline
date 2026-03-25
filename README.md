# E-Commerce Data Pipeline & Reporting 🛒📊

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458.svg)
![Data Engineering](https://img.shields.io/badge/Data-ETL_Pipeline-FF4B4B.svg)

## Overview
This repository contains an automated Python data pipeline built to process daily e-commerce transactions. 

Drawing from my experience managing digital storefronts and commercial operations, this script acts as a lightweight ETL (Extract, Transform, Load) tool. It ingests raw, unstructured sales data, cleans it, calculates key business metrics, and exports a production-ready daily report.

## ⚙️ Pipeline Architecture
* **Extract:** Ingests raw `.csv` order data (mock Shopify exports).
* **Transform (Data Cleaning):** * Identifies and drops incomplete records (e.g., missing Customer IDs).
  * Filters out invalid order statuses (e.g., 'Cancelled').
  * Dynamically calculates `Total_Value` (Quantity × Price).
* **Load/Report:** Generates an aggregated terminal summary (Total Revenue, AOV, Top Items) and exports a clean `daily_report.csv` for stakeholder use.

## 🚀 Running Locally
```bash
# Clone the repository
git clone [https://github.com/muathaf/ecommerce-data-pipeline.git](https://github.com/muathaf/ecommerce-data-pipeline.git)
cd ecommerce-data-pipeline

# Install dependencies
pip install pandas

# Execute the pipeline
python3 process_orders.py
