# Multinational Retail Data Centralisation

## Table of Content

- [Description](#description)
- [Installation instructions](#installation-instructions)
- [Usage instructions](#usage-instructions)
- [File structure](#file-structure)
- [License information](#license-information)

## Description

The project comprises three classes: DataExtractor, DatabaseConnector, and DataCleaning module. Each class serves a distinct purpose:

1. DataExtractor Class
   Functionality: Extracts data from various sources, such as RDS tables, PDFs, APIs, S3 buckets, and JSON files.
   Aim: Facilitates flexible and reusable data extraction methods for diverse use cases.
   Learning: Demonstrates the use of APIs, parallel processing, and data extraction from different sources.
2. DatabaseConnector Class
   Functionality: Connects to a database, lists tables, and uploads data to a specified table.
   Aim: Streamlines database operations and provides a modular approach to database connectivity.
   Learning: Highlights database connection, SQLAlchemy usage, and data upload to a relational database.
3. DataCleaning Module
   Functionality: Contains methods for cleaning and transforming data in various categories, such as user data, card data, store data, product data, order data, and date data.
   Aim: Ensures data cleanliness and standardization for further analysis or storage.
   Learning: Showcases data cleaning techniques, datetime conversions, and column manipulation.

### Aim:

To create a data extracting and cleaning tool.

## What I learned

- **Object-Oriented Programming (OOP):** Understanding of classes, methods, and attributes in Python.
- **Data Extraction Techniques:** Handling diverse data sources, including databases, PDFs, APIs, S3 buckets, and JSON files.
- **Database Operations:** Connecting to databases, querying tables, and uploading data using SQLAlchemy.
- **Data Cleaning and Transformation:** Techniques for cleaning and transforming data to meet specific requirements.
- **SQL Querying:** Proficiency in writing SQL queries to retrieve, filter, and manipulate data from relational databases.
- **Data Type Transformation:** Knowledge of converting and standardizing data types within SQL, such as changing column types and handling data type conversions.
- **Database Schema Understanding:** Understanding and working with the structure of a relational database, including tables, columns, and relationships.
- **Data Integrity:** Techniques for maintaining data integrity through constraints, data validation, and ensuring accurate data representation in the database.
- **Data Filtering and Aggregation:** Skill in using SQL to filter and aggregate data, enabling the extraction of meaningful insights from large datasets.
- **Database Maintenance:** Knowledge of routine database maintenance tasks, including updating records, adding new data, and ensuring consistent data quality.

## Installation instructions

Follow these steps to set up and run the project on your local machine.

### Prerequisites

Make sure you have the following software installed on your machine:

- [Python](https://www.python.org/) (version 3.12.0)

### Clone the Repository into a local folder

```bash
git clone https://github.com/gitYasir/multinational-retail-data-centralisation973 .
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage Instructions

#### Data Extraction:

Use the DataExtractor class to extract data from various sources.
Adjust parameters and endpoints as needed for specific use cases.

#### Database Operations:

Populate the db_creds.yaml and postgres_db_creds.yaml files with your database credentials.
Utilize the DatabaseConnector class to connect to a database and perform operations.

#### Data Cleaning:

Utilize the DataCleaning class for cleaning and transforming data in different categories.
Explore each cleaning method based on the type of data.

## File structure

- MNRDC/
  - data_cleaning.py
  - data_extraction.py
  - database_utils.py
  - db_creds.yaml
  - postgres_db_creds.yaml
  - products.csv
  - README.md
  - requirements.txt

## License information

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
