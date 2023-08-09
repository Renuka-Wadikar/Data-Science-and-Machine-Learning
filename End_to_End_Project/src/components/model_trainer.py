import pandas as pd
import numpy as np
from dataclasses import dataclass
import os
import sys

from src.logger import logging
from src.exception import CustomException
import src.utils as util

from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info('Entered into model training')
            logging.info('Split into train and test data')
            X_train,y_train ,X_test,y_test =(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
                )
            
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            
            model_report:dict = util.evaluate_model(X_train=X_train,
                                                    y_train=y_train,
                                                    X_test=X_test,
                                                    y_test=y_test,
                                                    models=models)
            
            logging.info(f'Model Report:{model_report}')
            #getting best model
            best_model_score = max(sorted(model_report.values()))
            
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]
            
            if best_model_score < 0.6:
                raise CustomException('No Best Model Found',sys)
            
            logging.info(f'Best Model is "{best_model_name}" with score {best_model_score} ')
            
            util.save_object(
                file_path=  self.model_trainer_config.trained_model_file_path,
                obj = best_model  
            )
            
            logging.info('Saved best Model!')
            
        except Exception as e:
            exp = CustomException(e,sys)
            logging.info(f'Exception Occured :{exp.error_msg}')


