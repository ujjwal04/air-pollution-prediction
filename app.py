from flask import Flask, render_template, url_for, request
import pandas as pd
import numpy as np
import os
import csv


import pickle

# load the model from disk
loaded_model = pickle.load(open('decision_regression_model.pkl', 'rb'))
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload-csv')
def uploadCSV():
    return render_template('upload-csv.html')


@app.route('/predictcsv', methods=['POST'])
def predictCSV():
    df = {}
    if request.method == 'POST':
        if request.files:
            # This line uses the same variable and worked fine
            uploaded_file = request.files['filename']
            filepath = os.path.join(
                app.config['FILE_UPLOADS'], uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath) as file:
                df = pd.read_csv(file)
    my_prediction = loaded_model.predict(df.iloc[:, :-1].values)
    my_prediction = my_prediction.tolist()
    data = []
    for i in my_prediction:
        data.append(i)
    return render_template("csv-result.html", prediction=my_prediction, data=data)


@app.route('/predict', methods=['POST'])
def predict():

    d = request.form.to_dict()
    df = pd.DataFrame([d.values()], columns=d.keys())
    my_prediction = loaded_model.predict(df)
    my_prediction = my_prediction.tolist()
    aqi_text = "MODERATE"
    aqi_desc = "DESC"
    aqi_color = "white"
    for i in my_prediction:
        if(i <= 50):
            aqi_text = "GOOD"
            aqi_desc = "Air quality is satisfactory, and air pollution poses little or no risk."
            aqi_color = "#2ecc71"
        elif(i > 50 and i <= 100):
            aqi_text = "MODERATE"
            aqi_desc = "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."
            aqi_color = "#f1c40f"
        elif(i > 100 and i <= 150):
            aqi_text = "UNHEALTHY FOR SENSITIVE GROUPS"
            aqi_desc = "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
            aqi_color = "#e67e22"
        elif(i > 150 and i <= 200):
            aqi_text = "UNHEALTHY"
            aqi_desc = "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."
            aqi_color = "#e74c3c"
        elif(i > 200 and i <= 300):
            aqi_text = "VERY UNHEALTHY"
            aqi_desc = "Health alert: The risk of health effects is increased for everyone."
            aqi_color = "#9b59b6"
        else:
            aqi_text = "HAZARDOUS"
            aqi_desc = "Health warning of emergency conditions: everyone is more likely to be affected."
            aqi_color = "#6F1E51"

    return render_template('result.html', prediction=my_prediction, aqi_desc=aqi_desc, aqi_text=aqi_text, aqi_color=aqi_color)


app.config['FILE_UPLOADS'] = "C:\\Users\\Ujjwal\\Documents"

if __name__ == '__main__':
    app.run(debug=True)
