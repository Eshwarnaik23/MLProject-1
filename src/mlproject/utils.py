import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging 
from urllib.parse import quote

# Load environment variables
load_dotenv()

# Fetch database credentials from .env
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

encoded_password = quote(password)

def read_sql_data():
    logging.info("Reading data from the database")
    try:
        # Use SQLAlchemy engine for connection
        connection_string = f"mysql+pymysql://{user}:{encoded_password}@{host}/{db}"
        engine = create_engine(connection_string)

        logging.info("Connection established successfully")
        
        # Execute query
        df = pd.read_sql_query("SELECT * FROM student", engine)
        print(df.head())  

        return df
        
    except Exception as ex:
        raise CustomException(str(ex), sys.exc_info())  
