import streamlit as st
import util.util as util
import base64

def add_bg_from_local(image_file):
    with open('/artifacts/images.jpg', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
        
    }}
    .block-container {{
         background-color: #ffffff;
        }}
    
    </style>
    """,
    unsafe_allow_html=True
    )


add_bg_from_local('/artifacts/images.jpg')


__predicted_price = None
util.load_saved_artifacts()
def predict_price(location,sqft,bath,bhk):
    global __predicted_price
    __predicted_price = util.get_estimated_price(location,float(sqft),float(bath),float(bhk))
    print('Predicted Value: ',__predicted_price)
    return __predicted_price
 
with st.container():
    st.title('Bengluru House Prediction')
    content = "This website is the frontend implementation of a Linear Regression model used for predicting Prices of Benguluru house predictions based on a Kaggle dataset"
    st.info(content)
    
    with st.form('my_form'):
        st.header('Select Location')
        locations = util.get_location_names()
        selected_location = st.selectbox(
            'location',
            options = locations,
            label_visibility='collapsed',
            key='location'
        )

        st.write('----')
        st.header('Total Sqft Area')
        total_sqft = st.number_input(
            label='sqft',
            label_visibility='collapsed',
            min_value= 300.00,
            key='sqft'   
        )

        st.write('----')
        st.header('Number of BHK')
        total_bhk = st.number_input(
            label='bhk',
            label_visibility='collapsed',
            min_value= 1,
            max_value= 13,
            step=1,
            key='bhk'  
        )

        st.write('----')
        st.header('Number of Bathrooms')
        total_bath = st.number_input(
            label='bath',
            label_visibility='collapsed',
            min_value= 1,
            max_value= 13,
            step=1,
            key='bath'  
        )

        predict = st.form_submit_button(
            'Predict',)
        if (predict):
            try:
                print('calling predict')
                price = predict_price(selected_location,total_sqft,total_bath,total_bhk)
                __predicted_price =f'The Estimated Cost of the house  is : {price} lakh rupees'
                st.write(__predicted_price)
            except:
                print('ERROR!!!')
                
        clear = st.form_submit_button(
            'Clear',)
        if (clear):
            __predicted_price = None
            
            



if __name__ == "__main__":
    print("Starting application....")
    #util.load_saved_artifacts()