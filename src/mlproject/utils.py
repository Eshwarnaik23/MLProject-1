import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging 
from urllib.parse import quote
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from src.mlproject.components.model_trainer import ModelTrainerConfig,ModelTrainer


import pickle
import numpy as np 


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


def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path,"wb")as file_obj:
            pickle.dump(obj,file_obj)
            
    except Exception as e:
        raise CustomException(e,sys)

def evalauate_models(X_train,y_train,X_test,y_test,param, models):
    ''' what this model does?
    ANS: Take all the algorithms and also the parameters and will fit
    and compute the r2 socre on train and test socore values will be put in dictonaries
    as key and value pair and return in the report.
    '''
    try:
        report={}
       
        for i in range(len(models)):
            model=list(models.values())[i]
            para=param[list(models.keys())[i]]
           
            gs= GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)
           
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
           
            #model.fit(X_train,y_train)
            #Train model
           
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
           
            train_model_score = r2_score(y_train,y_train_pred)
            
            test_model_score=r2_score(y_test,y_test_pred)
           
            report[list(models.keys())[i]]=test_model_score
           
        return report
    except Exception as e:
        raise CustomException( e,sys)
