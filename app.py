import numpy as np
import pandas as pd
import streamlit as st
import pickle
import json
import base64

with open('columns.json') as f:
  data = json.load(f)

__data_columns = data['data-columns']


pickle_in = open('bangalore_home_prices_model.pickle', 'rb')
classifier = pickle.load(pickle_in)

def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    return round(classifier.predict([x])[0],2)

def main():
    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
        
    add_bg_from_local('Real-Estate-Wallpaper_1.jpg')

    st.title('Bangalore House Price Predictor')
    st.write('Hello! Predict the price of a home in bangalore by entering the required details')\
    
    location=st.selectbox('Location', __data_columns[3:], key='good')
    area_sqft=st.text_input('Area (sq-ft)', max_chars=4)
    bath=st.text_input('No. of Bathrooms', max_chars=4)
    bedroom=st.text_input('No. of Bedrooms', max_chars=4)
    result=''

    if st.button('PREDICT'):
        result = get_estimated_price(location, area_sqft, bath, bedroom)
        st.success(f'The predicted price is {float(result)} lakhs')

if __name__=='__main__':
    main()