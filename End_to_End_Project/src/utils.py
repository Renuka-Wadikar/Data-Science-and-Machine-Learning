import os
import sys
import pandas as pd
import numpy as np
import dill

from src.logger import logging
from src.exception import CustomException

def save_object(file_path,obj):
    ''''
    Save the obj(preprocesing obj) to a the file path as pickle file
    '''
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path,'wb') as file:
            dill.dump(obj,file)
            
        logging.info(f'Saved Preprocessing object!')
        
    except Exception as e:
        exp = CustomException(e,sys)
        logging.info(f'ERROR Occured: {exp.error_msg}')
        raise exp