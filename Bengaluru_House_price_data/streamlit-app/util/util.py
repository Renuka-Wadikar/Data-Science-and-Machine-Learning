import json
import pickle
import numpy as np
import pandas as pd

#defining global variable
__locations = None
__data_col = None
__model = None

def get_location_names():
    return __locations

def get_estimated_price(location,sqft,bath,bhk):
    try:
        loc_index = __data_col.index(location.lower())
    except:
        loc_index = -1
    x =  np.zeros(len(__data_col))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)
    
    

def load_saved_artifacts():
    print('<<<<-----Loading Saved artifacts----->>>>')
    global __data_col
    global __locations
    global __model
    
    with open('./artifacts/columns.json','r') as file:
        __data_col = json.load(file)['data_columns']
        __locations = __data_col[3:]
        __locations = __locations + ['other']
        
    with open('./artifacts/banglore_price_prediction.pickle','rb') as f:
        __model = pickle.load(f)
    print('<<<<------Loading saved artifacts Sucess!!!---->>>>')


if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000,2,2))