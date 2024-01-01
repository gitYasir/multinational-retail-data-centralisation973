import numpy as np
import pandas as pd


class DataCleaning:
    """
    DataCleaning class provides methods for cleaning and transforming data.

    Methods:
    - clean_user_data(df): Cleans user-related data in the DataFrame.
    - clean_card_data(df): Cleans card-related data in the DataFrame.
    - clean_store_data(df): Cleans store-related data in the DataFrame.
    - convert_product_weights(df): Converts and standardizes product weights in the DataFrame.
    - clean_products_data(df): Cleans product-related data in the DataFrame.
    - clean_orders_data(df): Cleans order-related data in the DataFrame.
    - clean_dates_data(df): Cleans date-related data in the DataFrame.
    """

    def clean_user_data(self, df):
        """
        Cleans user-related data in the DataFrame.

        Parameters:
        - df (pd.DataFrame): DataFrame containing user-related data.

        Returns:
        - pd.DataFrame: Cleaned DataFrame.
        """
        df["first_name"] = df["first_name"].astype("string")
        df["last_name"] = df["last_name"].astype("string")
        df["company"] = df["company"].astype("string")
        df["address"] = df["address"].astype("string")
        df["country"] = df["country"].astype("string")
        df["country_code"] = df["country_code"].astype("string")
        df["phone_number"] = df["phone_number"].astype("string")
        df["country_code"] = df["country_code"].str.replace("GGB", "GB")
        df[["contact_number", "extension"]] = df["phone_number"].str.split(
            "x", n=1, expand=True
        )
        df = df.drop(columns=["phone_number"])
        df["extension"] = df["extension"].fillna("Not Applicable/Given")
        df["contact_number"] = df["contact_number"].str.replace("(", "")
        df["contact_number"] = df["contact_number"].str.replace(")", "")
        df["contact_number"] = df["contact_number"].str.replace("-", "")
        df["contact_number"] = df["contact_number"].str.replace(" ", "")
        df["contact_number"] = df["contact_number"].str.replace(".", "")
        df.loc[
            (df["contact_number"].str.startswith("+44"))
            & (df["contact_number"].str.len() < 13),
            "contact_number",
        ] = "Invalid Number"
        df["date_of_birth"] = pd.to_datetime(
            df["date_of_birth"], format="mixed", errors="coerce"
        )
        df["join_date"] = pd.to_datetime(
            df["join_date"], format="mixed", errors="coerce"
        )
        df.replace("NULL", np.nan, inplace=True)
        df.dropna(inplace=True)
        return df

    def clean_card_data(self, df):
        """
        Cleans card-related data in the DataFrame.

        Parameters:
        - df (pd.DataFrame): DataFrame containing card-related data.

        Returns:
        - pd.DataFrame: Cleaned DataFrame.
        """
        df["card_number"] = df["card_number"].astype("string")
        df["card_provider"] = df["card_provider"].astype("string")
        df["expiry_date"] = df["expiry_date"].astype("string")
        df["date_payment_confirmed"] = pd.to_datetime(
            df["date_payment_confirmed"], format="mixed", errors="coerce"
        )
        df["card_number"] = df["card_number"].str.strip("?")

        df.replace("NULL", np.nan, inplace=True)
        df.dropna(inplace=True)

        return df

    def clean_store_data(self, df):
        """
        Cleans store-related data in the DataFrame.

        Parameters:
        - df (pd.DataFrame): DataFrame containing store-related data.

        Returns:
        - pd.DataFrame: Cleaned DataFrame.
        """
        df["index"] = pd.to_numeric(df["index"], errors="coerce").astype("Int64")
        df["address"] = df["address"].astype("string")
        df["locality"] = df["locality"].astype("string")
        df["store_code"] = df["store_code"].astype("string")
        df["store_type"] = df["store_type"].astype("string")
        df["country_code"] = df["country_code"].astype("string")
        df["continent"] = df["continent"].astype("string")
        df["continent"] = df["continent"].str.lstrip("ee")
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
        df["staff_numbers"] = pd.to_numeric(
            df["staff_numbers"], errors="coerce"
        ).astype("Int64")
        df["opening_date"] = pd.to_datetime(
            df["opening_date"], format="mixed", errors="coerce"
        )
        values_to_exclude = [
            "13KJZ890JH",
            "NULL",
            "UXMWDMX1LC",
            "A3O5CBWAMD",
            "LACCWDI0SB",
            "VKA5I8H32X",
            "OXVE5QR07O",
            "2XE1OWOC23",
        ]
        df = df[~df["lat"].isin(values_to_exclude)]
        df = df.drop("lat", axis=1)
        return df

    def convert_product_weights(self, df):
        """
        Converts and standardizes product weights in the DataFrame.

        Parameters:
        - df (pd.DataFrame): DataFrame containing product-related data with weights.

        Returns:
        - pd.DataFrame: DataFrame with standardized product weights.
        """
        df["weight"] = df["weight"].astype("string", errors="ignore")
        df["weight"] = df["weight"].str.rstrip(" .")

        def process_ml_weights(weight):
            value = float(weight[:-2])
            to_kg = value / 1000
            return f"{to_kg}kg"

        def process_oz_weight(weight):
            value = float(weight[:-2])
            to_kg = value * 0.0283495
            return f"{to_kg}kg"

        def process_g_weight(weight):
            if "x" in weight and weight[:-2] != "kg":
                [num1, num2] = weight[:-1].split("x")
                res = float(num1) * float(num2)
                to_kg = res / 1000
                return f"{to_kg}kg"
            else:
                value = float(weight[:-1])
                to_kg = value / 1000
                return f"{to_kg}kg"

        df.loc[df["weight"].str.endswith("ml"), "weight"] = df.loc[
            df["weight"].str.endswith("ml"), "weight"
        ].apply(process_ml_weights)
        df.loc[df["weight"].str.endswith("oz"), "weight"] = df.loc[
            df["weight"].str.endswith("oz"), "weight"
        ].apply(process_oz_weight)
        df.loc[
            df["weight"].str.endswith("g") & ~df["weight"].str.endswith("kg"), "weight"
        ] = df.loc[
            df["weight"].str.endswith("g") & ~df["weight"].str.endswith("kg"), "weight"
        ].apply(
            process_g_weight
        )

        return df

    def clean_products_data(self, df):
        """
        Cleans product-related data in the DataFrame.

        Parameters:
        - df (pd.DataFrame): DataFrame containing product-related data.

        Returns:
        - pd.DataFrame: Cleaned DataFrame.
        """
        df = df.rename(columns={"Unnamed: 0": "index"})
        df["EAN"] = pd.to_numeric(df["EAN"], errors="coerce").astype("Int64")
        df["date_added"] = pd.to_datetime(
            df["date_added"], format="mixed", errors="coerce"
        )
        df["product_name"] = df["product_name"].astype("string")
        df["product_price"] = df["product_price"].astype("string")
        df["category"] = df["category"].astype("string")
        df["uuid"] = df["uuid"].astype("string")
        df["removed"] = df["removed"].astype("string")
        df["product_code"] = df["product_code"].astype("string")
        df.dropna(inplace=True)
        return df

    def clean_orders_data(self, df):
        """
        Cleans order-related data in the DataFrame.

        Parameters:
        - df (pd.DataFrame): DataFrame containing order-related data.

        Returns:
        - pd.DataFrame: Cleaned DataFrame.
        """
        df = df.drop(["first_name", "last_name", "1"], axis=1)
        df["date_uuid"] = df["date_uuid"].astype("string")
        df["user_uuid"] = df["user_uuid"].astype("string")
        df["store_code"] = df["store_code"].astype("string")
        df["product_code"] = df["product_code"].astype("string")
        return df

    def clean_dates_data(self, df):
        """
        Cleans date-related data in the DataFrame.

        Parameters:
        - df (pd.DataFrame): DataFrame containing date-related data.

        Returns:
        - pd.DataFrame: Cleaned DataFrame.
        """
        df["timestamp"] = df["timestamp"].astype("string")
        df["time_period"] = df["time_period"].astype("string")
        df["date_uuid"] = df["date_uuid"].astype("string")
        df["day"] = pd.to_numeric(df["day"], errors="coerce").astype("Int64")
        df["month"] = pd.to_numeric(df["month"], errors="coerce").astype("Int64")
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
        df.replace("NULL", np.nan, inplace=True)
        df.dropna(inplace=True)
        return df
