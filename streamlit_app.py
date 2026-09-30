import streamlit as st
import pandas as pd
import pickle

# Load the model and data
try:
    model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
    car = pd.read_csv('Cleaned_Car_data.csv')
except Exception as e:
    st.error(f"Error loading model or data: {e}")
    st.stop()

st.title("Car Price Prediction")
st.write("Enter the details of the car to predict its price.")

# Data processing for selectboxes
companies = sorted(car['company'].unique())
# The original app filtered models, wait, no it didn't filter dynamically in python but maybe in JS.
# Let's see if we can do dynamic filtering in Streamlit.
company = st.selectbox('Select Company', companies)

# Filter car models based on selected company
car_models_filtered = sorted(car[car['company'] == company]['name'].unique())
car_model = st.selectbox('Select Car Model', car_models_filtered)

# Year
# Original was: year = list(range(2026, 1994, -1))
# Let's get min and max year from data for better UX, or stick to range
year = st.selectbox('Select Year of Purchase', list(range(2026, 1994, -1)))

# Fuel Type
fuel_type = st.selectbox('Select Fuel Type', car['fuel_type'].unique())

# Kms Driven
kms_driven = st.number_input('Enter Number of Kilometers Driven', min_value=0, step=1000)

if st.button('Predict Price'):
    input_df = pd.DataFrame(
        {
            'name': [car_model],
            'company': [company],
            'year': [year],
            'kms_driven': [kms_driven],
            'fuel_type': [fuel_type]
        }
    )
    
    try:
        prediction = model.predict(input_df)
        st.success(f"The predicted price of the car is: ₹ {prediction[0]:,.2f}")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
