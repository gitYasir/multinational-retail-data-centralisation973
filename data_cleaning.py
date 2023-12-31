import numpy as np
import pandas as pd

from data_extraction import DataExtractor
from database_utils import DatabaseConnector


class DataCleaning:
    # def clean_user_data(self, df):
    #     # Turn the following columns to string format
    #     df["first_name"] = df["first_name"].astype("string")
    #     df["last_name"] = df["last_name"].astype("string")
    #     df["company"] = df["company"].astype("string")
    #     df["address"] = df["address"].astype("string")
    #     df["country"] = df["country"].astype("string")
    #     df["country_code"] = df["country_code"].astype("string")
    #     df["phone_number"] = df["phone_number"].astype("string")
    #     # Fix 'GGB' error
    #     df["country_code"] = df["country_code"].str.replace("GGB", "GB")
    #     # Split the phone number column into 'contact_number' and 'extension' columns
    #     df[["contact_number", "extension"]] = df["phone_number"].str.split(
    #         "x", n=1, expand=True
    #     )
    #     # Drop the unnecessary phone_number column
    #     df = df.drop(columns=["phone_number"])
    #     # Insert placeholder text into 'extension' column for numbers without an extension
    #     df["extension"] = df["extension"].fillna("Not Applicable/Given")
    #     # Replace (,),-, , and . with nothing in the contact_number column
    #     df["contact_number"] = df["contact_number"].str.replace("(", "")
    #     df["contact_number"] = df["contact_number"].str.replace(")", "")
    #     df["contact_number"] = df["contact_number"].str.replace("-", "")
    #     df["contact_number"] = df["contact_number"].str.replace(" ", "")
    #     df["contact_number"] = df["contact_number"].str.replace(".", "")
    #     # Find and replace all numbers that start with +44 and are less than 13 in length with Invalid Number
    #     df.loc[
    #         (df["contact_number"].str.startswith("+44"))
    #         & (df["contact_number"].str.len() < 13),
    #         "contact_number",
    #     ] = "Invalid Number"
    #     # Change the date_of_birth column from object to datetime65[ns]
    #     df["date_of_birth"] = pd.to_datetime(
    #         df["date_of_birth"], format="mixed", errors="coerce"
    #     )
    #     # Change the join_date column from object to datetime65[ns]
    #     df["join_date"] = pd.to_datetime(
    #         df["join_date"], format="mixed", errors="coerce"
    #     )
    #     # Replace all the 'NULL' values with numpys NaN
    #     df.replace("NULL", np.nan, inplace=True)
    #     # Drop all NaNs
    #     df.dropna(inplace=True)
    #     return df

    # def clean_card_data(self, df):
    #     # Change dtypes of to the appropriate type
    #     df["card_number"] = df["card_number"].astype("string")
    #     df["card_provider"] = df["card_provider"].astype("string")
    #     df["expiry_date"] = pd.to_datetime(
    #         df["expiry_date"], format="%m/%y", errors="coerce"
    #     )
    #     df["expiry_date"] = df["expiry_date"] + pd.offsets.MonthEnd(0)
    #     df["date_payment_confirmed"] = pd.to_datetime(
    #         df["date_payment_confirmed"], format="mixed", errors="coerce"
    #     )
    #     # Remove the '?' from the card numbers
    #     df["card_number"] = df["card_number"].str.strip("?")
    #     # Select and format the card numbers that are 17 or 19 digits long
    #     df.loc[
    #         (df["card_number"].str.len() >= 17) & (df["card_number"].str.len() <= 19),
    #         "card_number",
    #     ] = df.loc[
    #         (df["card_number"].str.len() >= 17) & (df["card_number"].str.len() <= 19),
    #         "card_number",
    #     ].apply(
    #         lambda x: x[0:4]
    #         + " "
    #         + x[4:8]
    #         + " "
    #         + x[8:12]
    #         + " "
    #         + x[12:16]
    #         + " "
    #         + x[16:20]
    #     )

    #     # Select and format the card numbers that are 13 or 16 digits long
    #     df.loc[
    #         (df["card_number"].str.len() >= 13) & (df["card_number"].str.len() <= 16),
    #         "card_number",
    #     ] = df.loc[
    #         (df["card_number"].str.len() >= 13) & (df["card_number"].str.len() <= 16),
    #         "card_number",
    #     ].apply(
    #         lambda x: x[0:4] + " " + x[4:8] + " " + x[8:12] + " " + x[12:16]
    #     )

    #     # Select and format the card numbers that are 11 or 12 digits long
    #     df.loc[
    #         (df["card_number"].str.len() >= 11) & (df["card_number"].str.len() <= 12),
    #         "card_number",
    #     ] = df.loc[
    #         (df["card_number"].str.len() >= 11) & (df["card_number"].str.len() <= 12),
    #         "card_number",
    #     ].apply(
    #         lambda x: x[0:4] + " " + x[4:8] + " " + x[8:12]
    #     )

    #     # Select and format the one card number that 9 digits long
    #     df.loc[
    #         (df["card_number"].str.len() == 9),
    #         "card_number",
    #     ] = df.loc[
    #         (df["card_number"].str.len() == 9),
    #         "card_number",
    #     ].apply(lambda x: x[0:3] + " " + x[3:6] + " " + x[6:9])

    #     # Replace all the 'NULL' values with numpys NaN
    #     df.replace("NULL", np.nan, inplace=True)
    #     # Drop all NaNs
    #     df.dropna(inplace=True)

    #     return df

    # def clean_store_data(self, df):
    #     df = df.drop("lat", axis=1)
    #     df = df.drop(0, axis=1)
    #     df["index"] = pd.to_numeric(df["index"], errors="coerce").astype("Int64")
    #     df["address"] = df["address"].astype("string")
    #     df["locality"] = df["locality"].astype("string")
    #     df["store_code"] = df["store_code"].astype("string")
    #     df["store_type"] = df["store_type"].astype("string")
    #     df["country_code"] = df["country_code"].astype("string")
    #     df["continent"] = df["continent"].astype("string")
    #     df["continent"] = df["continent"].str.lstrip("ee")
    #     df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    #     df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    #     df["staff_numbers"] = pd.to_numeric(
    #         df["staff_numbers"], errors="coerce"
    #     ).astype("Int64")
    #     df["opening_date"] = pd.to_datetime(
    #         df["opening_date"], format="mixed", errors="coerce"
    #     )
    #     # Replace all the 'NULL' values with numpys NaN
    #     df.replace("NULL", np.nan, inplace=True)
    #     # Drop all NaNs
    #     df.dropna(inplace=True)
    #     return df

    # def convert_product_weights(self, df):
    #     df["weight"] = df["weight"].astype("string", errors="ignore")

    #     def process_ml_weights(weight):
    #         value = float(weight[:-2])
    #         to_kg = value / 1000
    #         return f"{to_kg}kg"

    #     def process_oz_weight(weight):
    #         value = float(weight[:-2])
    #         to_kg = value * 0.0283495
    #         return f"{to_kg}kg"

    #     def process_g_weight(weight):
    #         if "x" in weight:
    #             [num1, num2] = weight[:-1].split("x")
    #             res = float(num1) * float(num2)
    #             to_kg = res / 1000
    #             return f"{to_kg}kg"
    #         else:
    #             value = float(weight[:-1])
    #             to_kg = value / 1000
    #             return f"{to_kg}kg"

    #     df.loc[df["weight"].str.endswith("ml"), "weight"] = df.loc[
    #         df["weight"].str.endswith("ml"), "weight"
    #     ].apply(process_ml_weights)
    #     df.loc[df["weight"].str.endswith("oz"), "weight"] = df.loc[
    #         df["weight"].str.endswith("oz"), "weight"
    #     ].apply(process_oz_weight)
    #     df.loc[
    #         df["weight"].str.endswith("g") & ~df["weight"].str.endswith("kg"), "weight"
    #     ] = df.loc[
    #         df["weight"].str.endswith("g") & ~df["weight"].str.endswith("kg"), "weight"
    #     ].apply(
    #         process_g_weight
    #     )

    #     return df

    # def clean_products_data(self, df):
    #     df = df.rename(columns={"Unnamed: 0": "index"})
    #     df["EAN"] = pd.to_numeric(df["EAN"], errors="coerce").astype("Int64")
    #     df["date_added"] = pd.to_datetime(
    #         df["date_added"], format="mixed", errors="coerce"
    #     )
    #     df["product_name"] = df["product_name"].astype("string")
    #     df["product_price"] = df["product_price"].astype("string")
    #     df["category"] = df["category"].astype("string")
    #     df["uuid"] = df["uuid"].astype("string")
    #     df["removed"] = df["removed"].astype("string")
    #     df["product_code"] = df["product_code"].astype("string")
    #     # # Replace all the 'NULL' values with numpys NaN
    #     # df.replace("NULL", np.nan, inplace=True)
    #     # Drop all NaNs
    #     df.dropna(inplace=True)
    # return df

    # def clean_orders_data(self, df):
    #     df = df.drop(["first_name", "last_name", "1"], axis=1)
    #     df["date_uuid"] = df["date_uuid"].astype("string")
    #     df["user_uuid"] = df["user_uuid"].astype("string")
    #     df["store_code"] = df["store_code"].astype("string")
    #     df["product_code"] = df["product_code"].astype("string")
    #     return df

    def clean_dates_data(self, df):
        months = range(1, 13)
        df["timestamp"] = df["timestamp"].astype("string")
        df["time_period"] = df["time_period"].astype("string")
        df["date_uuid"] = df["date_uuid"].astype("string")
        df["day"] = pd.to_numeric(df["day"], errors="coerce").astype(
            "Int64"
        )  # Replace all the 'NULL' values with numpys NaN
        df["month"] = pd.to_numeric(df["month"], errors="coerce").astype(
            "Int64"
        )  # Replace all the 'NULL' values with numpys NaN
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype(
            "Int64"
        )  # Replace all the 'NULL' values with numpys NaN
        df.replace("NULL", np.nan, inplace=True)
        # Drop all NaNs
        df.dropna(inplace=True)
        return df


connector = DatabaseConnector()
extractor = DataExtractor()
cleaning = DataCleaning()

dates_data = extractor.extract_from_json(
    "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"
)

# pd.set_option("display.max_rows", None)
cleaned_dates_df = cleaning.clean_dates_data(dates_data)


# region
# connector.read_db_creds()
# connector.init_db_engine()
# tables = connector.list_db_tables()
# users_table = tables[1]
# connector.read_db_creds()
# connector.init_db_engine()
# tables = connector.list_db_tables()
# orders_table = tables[2]
# orders_data = extractor.read_rds_table(connector, orders_table)

# cleaned_orders_table_df = cleaning.clean_orders_data(orders_data)
# connector.upload_to_db(cleaned_orders_table_df,'orders_table')
# users_data = extractor.read_rds_table(connector, users_table)
# cards_data = extractor.retrieve_pdf_data(
#     "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
# )
# headers = {
#     "x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX",
# }
# store_numbers_url = (
#     "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
# )
# extractor.list_number_of_stores(store_numbers_url, headers)

# store_url = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details"
# stores_data = extractor.retrieve_stores_data(store_url, headers)

# s3_url = "s3://data-handling-public/products.csv"
# products_df = extractor.extract_from_s3(s3_url)

# cleaned_users_data = cleaning.clean_user_data(users_data)
# cleaned_cards_data = cleaning.clean_card_data(cards_data)
# cleaned_stores_data = cleaning.clean_store_data(stores_data)
# cleaned_weights = cleaning.convert_product_weights(products_df)
# cleaned_products_df = cleaning.clean_products_data(cleaned_weights)

# connector.upload_to_db(cleaned_users_data, "dim_users")
# connector.upload_to_db(cleaned_cards_data, "dim_card_details")
# connector.upload_to_db(cleaned_stores_data, "dim_store_details")
# connector.upload_to_db(cleaned_products_df, "dim_products")
# endregion
