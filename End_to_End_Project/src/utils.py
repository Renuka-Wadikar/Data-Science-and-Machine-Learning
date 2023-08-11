import os
import sys
import pandas as pd
import numpy as np
import dill

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

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
    
def evaluate_model(X_train,y_train,X_test,y_test,models,params):
    '''
    Evaluate each model in turn and store results
    '''
    try:
        report = {}
        
        for i in range(len(list(models))):
            model = list(models.values())[i]
            
            param = params[list(models.keys())[i]]
            
            gs =GridSearchCV(model,param_grid=param,cv=4)
            gs.fit(X_train,y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train) #trainning the model
            
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score
        logging.info('Evalulation of model Completed!')
        return report

    except Exception as e:
        exp = CustomException(e,sys)
        logging.info(f'ERROR Occured: {exp.error_msg}')
        raise exp