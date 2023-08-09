import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd


from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer




@dataclass
class DataIngestionConfig:
    '''
    any type of input  data is provided from this class
    '''
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','raw.csv')
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def init_data_ingestion(self):
        logging.info('Entered the data ingestion component')
        try:
            
            FILEPATH = "../../notebook/data/stud.csv"
            data = pd.read_csv(FILEPATH)  
            
            logging.info('Read the dataset as dataframe : data')
          
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            data.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            train_set,test_set = train_test_split(data,test_size=0.2,random_state=42)
            logging.info('Train-Test split completed')
        
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            logging.info('Ingestion of Data is completed')
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except Exception as e:
            exp =  CustomException(e,sys)
            logging.info(f'Exception occur:\n{exp.error_msg}')
            raise exp
        

if __name__=="__main__":
    objDataIngest = DataIngestion()
    train_data,test_data = objDataIngest.init_data_ingestion()
    
    
    data_transformation = DataTransformation()
    train_arr , test_arr,preprocess_path  = data_transformation.initiate_data_transformation(train_data,test_data)
   
    model_train = ModelTrainer()
    print(model_train.initiate_model_trainer(train_arr,test_arr))
    