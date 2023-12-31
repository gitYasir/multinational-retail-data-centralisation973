import yaml
from sqlalchemy import Date, create_engine, inspect


class DatabaseConnector:
    def read_db_creds(self):
        with open("db_creds.yaml", "r") as creds_data:
            creds = yaml.safe_load(creds_data)
            return creds

    def init_db_engine(self):
        creds = self.read_db_creds()
        engine = create_engine(
            f'{creds["RDS_DATABASE_TYPE"]}+{creds["RDS_DBAPI"]}://{creds["RDS_USER"]}:{creds["RDS_PASSWORD"]}@{creds["RDS_HOST"]}:{creds["RDS_PORT"]}/{creds["RDS_DATABASE"]}'
        )
        engine.execution_options(isolation_level="AUTOCOMMIT").connect()
        return engine

    def list_db_tables(self):
        engine = self.init_db_engine()
        inspector = inspect(engine)
        inspector.get_table_names()
        return inspector.get_table_names()

    def upload_to_db(self, dataframe, table_name):
        with open("postgres_db_creds.yaml", "r") as creds_data:
            creds = yaml.safe_load(creds_data)
        engine = create_engine(f'{creds['DATABASE_TYPE']}://{creds['USER']}:{creds['PASSWORD']}@{creds['HOST']}:{creds['PORT']}/{creds['DATABASE_NAME']}')
        # Find the columns with the datetime64[ns] dtype
        datetime_columns = dataframe.select_dtypes(include='datetime64[ns]').columns
        # Change each one to be DATE type ready for SQL upload
        dtype_mapping = {column: Date() for column in datetime_columns}
        # Upload to SQL DB 
        dataframe.to_sql(table_name, engine, if_exists="replace", index=False,dtype=dtype_mapping)


connector = DatabaseConnector()

connector.read_db_creds()
connector.init_db_engine()
connector.list_db_tables()
