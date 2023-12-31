from concurrent.futures import ThreadPoolExecutor

import boto3
import pandas as pd
import requests
import tabula
from sqlalchemy import text


class DataExtractor:
    """
    DataExtractor class provides methods for extracting data from various sources.

    Methods:
    - read_rds_table(database_connector, table_name): Reads data from an RDS table.
    - retrieve_pdf_data(link): Retrieves data from a PDF file specified by the link.
    - list_number_of_stores(number_of_stores_endpoint, headers_dictionary): Lists the number of stores.
    - retrieve_stores_data(store_endpoint, headers_dictionary): Retrieves data for multiple stores.
    - extract_from_s3(s3_link): Extracts data from an S3 bucket specified by the link.
    - extract_from_json(link): Extracts data from a JSON file specified by the link.
    """

    def read_rds_table(self, database_connector, table_name):
        """
        Reads data from an RDS table.

        Parameters:
        - database_connector (DatabaseConnector): An instance of the DatabaseConnector class.
        - table_name (str): Name of the table to read data from.

        Returns:
        - pd.DataFrame: A DataFrame containing the data from the specified table.
        """
        database_connector.read_db_creds()
        engine = database_connector.init_db_engine()

        if table_name not in database_connector.list_db_tables():
            print(f"Error: Table '{table_name}' not found.")
            return None

        query = f"SELECT * FROM {table_name}"

        with engine.connect() as connection:
            result = connection.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df

    def retrieve_pdf_data(self, link):
        """
        Retrieves data from a PDF file specified by the link.

        Parameters:
        - link (str): URL or file path to the PDF.

        Returns:
        - pd.DataFrame: A DataFrame containing the data extracted from the PDF.
        """
        dfs = tabula.read_pdf(link, pages="all")
        df = pd.concat(dfs, ignore_index=True)
        return df

    def list_number_of_stores(self, number_of_stores_endpoint, headers_dictionary):
        """
        Lists the number of stores.

        Parameters:
        - number_of_stores_endpoint (str): API endpoint to get the number of stores.
        - headers_dictionary (dict): Headers for the API request.

        Returns:
        - int: Number of stores.
        """
        response = requests.get(number_of_stores_endpoint, headers=headers_dictionary)
        data = response.json()
        return data["number_stores"]

    def retrieve_stores_data(self, store_endpoint, headers_dictionary):
        """
        Retrieves data for multiple stores using parallel processing.

        Parameters:
        - store_endpoint (str): API endpoint to retrieve store data.
        - headers_dictionary (dict): Headers for the API request.

        Returns:
        - pd.DataFrame: A DataFrame containing the data of multiple stores.
        """
        store_numbers = range(1, 452)
        stores = pd.DataFrame()
        with ThreadPoolExecutor() as executor:
            responses = executor.map(
                lambda store_number: requests.get(
                    f"{store_endpoint}/{store_number}", headers=headers_dictionary
                ),
                store_numbers,
            )

        for response in responses:
            store_data = response.json()
            stores = pd.concat([stores, pd.DataFrame([store_data])], ignore_index=True)

        return stores

    def extract_from_s3(self, s3_link):
        """
        Extracts data from an S3 bucket specified by the link.

        Parameters:
        - s3_link (str): S3 link in the format 's3://bucket_name/file_path'.

        Returns:
        - pd.DataFrame: A DataFrame containing the data from the specified S3 file.
        """
        s3 = boto3.client("s3")
        s3_link = s3_link.replace("s3://", "")
        [bucket, file] = s3_link.split("/")
        s3.download_file(
            bucket, file, "/Users/DELL/OneDrive/Desktop/MNRDC/products.csv"
        )
        df = pd.read_csv("./products.csv")
        return df

    def extract_from_json(self, link):
        """
        Extracts data from a JSON file specified by the link.

        Parameters:
        - link (str): URL or file path to the JSON file.

        Returns:
        - pd.DataFrame: A DataFrame containing the data from the specified JSON file.
        """
        dates_data = pd.read_json(link)
        return dates_data
