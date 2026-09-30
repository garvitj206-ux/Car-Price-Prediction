import pandas as pd
from flask import Flask, render_template,request
import pickle

app = Flask(__name__)

model = pickle.load(open('LinearRegressionModel.pkl','rb'))
car = pd.read_csv("Cleaned_Car_data.csv")
@app.route('/')
def index():
    companies = sorted(car["company"].unique())
    car_models = sorted(car["name"].unique())
    year = list(range(2026, 1994, -1))
    fuel_type = car["fuel_type"].unique()
    return render_template('index.html',companies = companies, car_models = car_models, year = year, fuel_type = fuel_type)

@app.route('/predict', methods=['POST'])
def predict():
    company =request.form.get('company')
    car_models =request.form.get('car_models')
    year =int(request.form.get('year'))
    fuel_type =request.form.get('fuel_type')
    kms_drive =int(request.form.get('kms_driven'))
    print(company,car_models,year,fuel_type,kms_drive)

    input_df = pd.DataFrame(
        {
            'name': [car_models],
            'company': [company],
            'year': [year],
            'kms_driven': [kms_drive],
            'fuel_type': [fuel_type]
        }
    )

    prediction = model.predict(input_df)
    return str(prediction[0])
if __name__ == '__main__':
    app.run(debug=True)
