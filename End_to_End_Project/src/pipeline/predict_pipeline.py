import sys
import pandas as pd
import numpy as np
import os

from src.logger import logging
from src.exception import CustomException
from src.utils import load_objects

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self,features):
        try:
            current_path = os.getcwd()

            model_path =os.path.join(current_path,'src','components','artifacts','model.pkl')
            preprocessor_path =os.path.join(current_path,'src','components','artifacts','preprocessor.pkl')
            
            logging.info(f'Loading the model started..')
            model = load_objects(file_path=model_path)
            preprocessor = load_objects(file_path=preprocessor_path)
            logging.info(f'Loading the model sucess!..')
            
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        except Exception as e:
            exp = CustomException(e,sys)
            logging.info(f'Exception Occured: {exp.error_msg}')
            raise exp
    
class CustomData:
    def __init__(self,
                 gender: str,
                 race_ethnicity:str,
                 parental_level_of_education:str,
                 lunch:str,
                 test_preparation_course:str,
                 reading_score:int,
                 writing_score:int):
        self.gender = gender
        self.race_ethnicity=race_ethnicity
        self.parental_level_of_education=parental_level_of_education
        self.lunch=lunch
        self.test_preparation_course=test_preparation_course
        self.reading_score=reading_score
        self.writing_score = writing_score
        
    def get_data_as_dataFrame(self):
        try:
            custom_data_input_dict = {
                "gender":[self.gender],
                "race_ethnicity" : [self.race_ethnicity],
                "parental_level_of_education":[self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
                
            }
            
            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            exp = CustomException(e,sys)
            logging.info(f'Exception Occured: {exp.error_msg}')
            raise exp
        
    