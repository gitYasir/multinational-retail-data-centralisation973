from concurrent.futures import ThreadPoolExecutor

import boto3
import pandas as pd
import requests
import tabula
from sqlalchemy import text

from database_utils import DatabaseConnector


class DataExtractor:
    def read_rds_table(self, database_connector, table_name):
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
        dfs = tabula.read_pdf(link, pages="all")
        df = pd.concat(dfs, ignore_index=True)
        return df

    def list_number_of_stores(self, number_of_stores_endpoint, headers_dictionary):
        response = requests.get(number_of_stores_endpoint, headers=headers_dictionary)
        data = response.json()
        return data["number_stores"]

    def retrieve_stores_data(self, store_endpoint, headers_dictionary):
        store_numbers = range(1, 452)
        stores = pd.DataFrame()
        with ThreadPoolExecutor() as executor:
            # Use executor.map to parallelize the requests
            responses = executor.map(
                lambda store_number: requests.get(
                    f"{store_endpoint}/{store_number}", headers=headers_dictionary
                ),
                store_numbers,
            )

        for response in responses:
            # response = requests.get(
            #     f"{store_endpoint}/{store_num}", headers=headers_dictionary
            # )
            store_data = response.json()
            stores = pd.concat([stores, pd.DataFrame([store_data])], ignore_index=True)

        return stores

    def extract_from_s3(self, s3_link):
        # s3://data-handling-public/products.csv
        s3 = boto3.client("s3")
        s3_link = s3_link.replace("s3://", "")
        [bucket, file] = s3_link.split("/")
        s3.download_file(
            bucket, file, "/Users/DELL/OneDrive/Desktop/MNRDC/products.csv"
        )
        df = pd.read_csv("./products.csv")
        return df

    def extract_from_json(self, link):
        dates_data = pd.read_json(link)
        return dates_data


connector = DatabaseConnector()
# connector.read_db_creds()
# connector.init_db_engine()
# tables = connector.list_db_tables()
# users_table = tables[1]


extractor = DataExtractor()
# extractor.read_rds_table(connector, users_table)
# extractor.retrieve_pdf_data(
#     "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
# )
pd.set_option("display.max_rows", None)

# store_numbers_url = (
#     "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
# )
# headers = {
#     "x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX",
# }
# extractor.list_number_of_stores(store_numbers_url,headers)

# store_url = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details"
# print(extractor.retrieve_stores_data(store_url, headers))

s3_url = "s3://data-handling-public/products.csv"
extractor.extract_from_s3(s3_url)
