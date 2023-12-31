import yaml
from sqlalchemy import Date, create_engine, inspect


class DatabaseConnector:
    """
    DatabaseConnector class facilitates database connection and operations.

    Methods:
    - read_db_creds(): Reads the database credentials from a YAML file.
    - init_db_engine(): Initializes a database engine using the obtained credentials.
    - list_db_tables(): Lists the tables present in the connected database.
    - upload_to_db(dataframe, table_name): Uploads a DataFrame to a specified table in the database.
    """

    def read_db_creds(self):
        """
        Reads the database credentials from a YAML file.

        Returns:
        - dict: A dictionary containing database connection credentials.
        """
        with open("db_creds.yaml", "r") as creds_data:
            creds = yaml.safe_load(creds_data)
            return creds

    def init_db_engine(self):
        """
        Initializes a database engine using the obtained credentials.

        Returns:
        - sqlalchemy.engine.base.Engine: An SQLAlchemy engine object for database operations.
        """
        creds = self.read_db_creds()
        engine = create_engine(
            f'{creds["RDS_DATABASE_TYPE"]}+{creds["RDS_DBAPI"]}://{creds["RDS_USER"]}:{creds["RDS_PASSWORD"]}@{creds["RDS_HOST"]}:{creds["RDS_PORT"]}/{creds["RDS_DATABASE"]}'
        )
        engine.execution_options(isolation_level="AUTOCOMMIT").connect()
        return engine

    def list_db_tables(self):
        """
        Lists the tables present in the connected database.

        Returns:
        - list: A list of table names in the connected database.
        """
        engine = self.init_db_engine()
        inspector = inspect(engine)
        return inspector.get_table_names()

    def upload_to_db(self, dataframe, table_name):
        """
        Uploads a DataFrame to a specified table in the database.

        Parameters:
        - dataframe (pd.DataFrame): The DataFrame to be uploaded.
        - table_name (str): Name of the table in the database.

        Note: Assumes that the DataFrame contains datetime columns, and it converts them to DATE type for SQL upload.

        Returns:
        - None
        """
        with open("postgres_db_creds.yaml", "r") as creds_data:
            creds = yaml.safe_load(creds_data)
        engine = create_engine(
            f'{creds["DATABASE_TYPE"]}://{creds["USER"]}:{creds["PASSWORD"]}@{creds["HOST"]}:{creds["PORT"]}/{creds["DATABASE_NAME"]}'
        )

        datetime_columns = dataframe.select_dtypes(include="datetime64[ns]").columns
        dtype_mapping = {column: Date() for column in datetime_columns}
        dataframe.to_sql(
            table_name, engine, if_exists="replace", index=False, dtype=dtype_mapping
        )
