from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import pandas as pd
import os
import pickle
import joblib
import numpy as np
import pandas as pd
from fastai.vision.all import *
import requests

app = Flask(__name__)
app.secret_key = 'secretKEY'

#Set database location
app.config['DATABASE'] = 'database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

conn=sqlite3.connect(app.config['DATABASE'])
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users
            (userid INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT,
            mobile TEXT,
            DOB TEXT,
            soil TEXT,
            landLocation TEXT,
            landSize TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS records 
            (recordid INTEGER PRIMARY KEY AUTOINCREMENT, 
            userId INTEGER,
            season TEXT,
            crop TEXT,
            yield TEXT,
            expenses TEXT,
            income TEXT,
            pesticide TEXT,
            fertilizer TEXT,
            weather TEXT,
            date TEXT
            )''')


conn.commit()
conn.close()

def get_weather(api_key, city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return temperature, humidity
    else:
        print("Error:", data['message'])
        return None, None
    
api_key = '5138d66fbb91acdb14176da6d4c2e4e0'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/auth', methods=["GET"])
def auth():
    return render_template('auth.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    conn=sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE mobile = ? AND DOB = ?", (data['mobile'],data['DOB']))
    rec=cur.fetchone()
    print(rec)
    print(data['mobile'],data['DOB'])
    conn.close()
    if rec:
        session['userid'] = rec[0]
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('auth'))

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        conn=sqlite3.connect(app.config['DATABASE'])
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, mobile, DOB, soil, landLocation, landSize) VALUES (?,?,?,?,?,?)",
                    (data['name'], data['mobile'], data['DOB'], data['soil'], data['landLocation'], data['landSize']))
        conn.commit()

        cur.execute("SELECT * FROM users WHERE mobile = ? & DOB = ?", (data['mobile'],data['DOB']))
        rec=cur.fetchone()
        conn.close()
        if rec:
            session['userid'] = rec[0]
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('auth'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'userid' not in session:
        return render_template('index.html')
    userid = session['userid']
    conn=sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT name FROM users WHERE userid = ?", (userid,))
    name = cur.fetchone()[0]

    cur.execute("SELECT * FROM records WHERE userId = ?", (userid,))
    records = cur.fetchall()
    conn.close()

    #Convert the records to a pandas df
    df = pd.DataFrame(records, columns=['recordid', 'userId', 'season', 'crop', 'yield', 'expenses', 'income', 'pesticide', 'fertilizer', 'weather', 'date'])
    df['date'] = pd.to_datetime(df['date'])
    df['yield'] = df['yield'].astype(int)
    df['expenses'] = df['expenses'].astype(int)
    df['income'] = df['income'].astype(int)
    #Plot a bar graph for yield over time
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['date'], y=df['yield']))
    fig.update_layout(title='Yield over time', xaxis_title='Date', yaxis_title='Yield')
    yield_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    #Plot a pie chart for crop based on yield
    crop_yield = df.groupby('crop')['yield'].sum().reset_index()
    fig = go.Figure(data=[go.Pie(labels=crop_yield['crop'], values=crop_yield['yield'])])
    fig.update_layout(title='Crop yield distribution')
    crop_yield_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    #Plot a bar chart for crop based on profit which is equal to income - expenses
    df['profit'] = df['income'] - df['expenses']
    crop_profit = df.groupby('crop')['profit'].sum().reset_index()
    fig = go.Figure(data=[go.Bar(x=crop_profit['crop'], y=crop_profit['profit'])])
    fig.update_layout(title='Crop profit distribution', xaxis_title='Crop', yaxis_title='Profit')
    crop_profit_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    df = df.sort_values(by='date')
    #Plot a line chart for profit over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['profit'], mode='lines+markers'))
    fig.update_layout(title='Profit over time', xaxis_title='Date', yaxis_title='Profit')
    profit_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    total_income = df['income'].sum()
    total_expenses = df['expenses'].sum()
    total_yield = df['yield'].sum()
    total_profit = int(total_income) - int(total_expenses)

    return render_template('dashboard.html', name=name, yield_chart=yield_chart ,crop_yield_chart=crop_yield_chart, crop_profit_chart = crop_profit_chart, profit_chart = profit_chart, total_income=total_income, total_expenses=total_expenses, total_yield=total_yield, total_profit=total_profit)

@app.route('/records', methods=['GET','POST'])
def records():
    if 'userid' not in session:
        return render_template('index.html')
    if request.method == 'POST':
        data = request.form
        conn=sqlite3.connect(app.config['DATABASE'])
        cur = conn.cursor()
        cur.execute("INSERT INTO records (userId, season, crop, yield, expenses, income, pesticide, fertilizer, weather, date) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (session['userid'], data['Season'], data['Crop'], data['Yield'], data['Expenses'], data['Income'], data['PesticideUsed'], data['FertilizerUsed'], data['Weather'], data['Date']))
        conn.commit()
        conn.close()
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT recordid, season, crop, yield, expenses, income, fertilizer, pesticide, date, weather FROM records WHERE userId = ?", (session['userid'],))
    records = cur.fetchall()
    conn.close()
    return render_template('records.html', records=records)

@app.route('/disease', methods=['GET','POST'])
def disease():
    if 'userid' not in session:
        return render_template('index.html')
    if request.method=="POST":
        
        image = request.files['cropImg']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], str(session['userid'])+'_'+image.filename))

        model = joblib.load('diseaseModel.joblib')
        test_dl = model.dls.test_dl([app.config['UPLOAD_FOLDER']+'/'+str(session['userid'])+'_'+image.filename])
        preds, _ = model.get_preds(dl=test_dl)
        

        preds = F.softmax(preds, dim=1)

        damage_classes = model.dls.vocab
        damage_labels = list(damage_classes)

        # Get the predicted probabilities for each class
        predicted_probabilities = preds[0].tolist()
        predicted_probabilities = [round(p*100, 2) for p in predicted_probabilities]
        # Create a dictionary to associate each damage class with its predicted probability
        prediction_dict = dict(zip(damage_labels, predicted_probabilities))

        # Sort the dictionary based on probabilities in descending order
        sorted_predictions = sorted(prediction_dict.items(), key=lambda x: x[1], reverse=True)

        # Display the predictions
        for damage_class, probability in sorted_predictions:
            print(f"{damage_class}: {probability:.4f}")
        
        return render_template('disease.html', disease=sorted_predictions)
    return render_template('disease.html')

@app.route('/yield', methods=['GET','POST'])
def yield_prediction():
    if 'userid' not in session:
        return render_template('index.html')
    if request.method == 'POST':
        data = request.form
        model = joblib.load('yieldModel.pkl')
        df=pd.DataFrame([data])
        df = df.apply(pd.to_numeric).astype(float)
        print(df.iloc[0].values.reshape(1, -1))
        prediction = model.predict(df.iloc[0].values.reshape(1, -1))[0]
        return render_template('yield.html', prediction=prediction)
    return render_template('yield.html')

@app.route('/fertilizer', methods=['GET','POST'])
def fertilizer_recommendation():
    if 'userid' not in session:
        return render_template('index.html')
    if request.method == 'POST':
        data = request.form
        df = pd.DataFrame([data])

        soil_encoder = joblib.load('soilEncoder.pkl')
        crop_encoder = joblib.load('cropEncoder.pkl')
        fertilizer_encoder = joblib.load('fertilizerEncoder.pkl')

        fertilizer_model = joblib.load('fertilizerModel.pkl')

        df['soil'] = soil_encoder.transform(df['soil'])
        df['crop'] = crop_encoder.transform(df['crop'])

        df = df.apply(pd.to_numeric).astype(int)

        pred = fertilizer_model.predict(df.iloc[0].values.reshape(1, -1))
        prediction = fertilizer_encoder.inverse_transform(pred)[0]
        
        return render_template('fertilizer.html', prediction=prediction)
    return render_template('fertilizer.html')

@app.route('/weather', methods=['GET','POST'])
def weather():
    if request.method == 'POST':
        data = request.form
        city_name = data['City']
        temperature, humidity = get_weather(api_key, city_name)

        df = pd.DataFrame([{ 'N': data['N'], 'P': data['P'], 'K': data['K'], 'temperature': temperature, 'humidity': humidity, 'ph': data['ph'], 'rainfall': data['rainfall']}])
        df = df.apply(pd.to_numeric).astype(float)
        scaler = joblib.load('CropPredScaler.pkl')
        df = scaler.transform(df)
        print(df)
        crop_pred = joblib.load('CropPred.pkl')
        prediction = crop_pred.predict(df)[0]

        cat_code = joblib.load('targets.pkl')
        prediction = cat_code[prediction]
        print(prediction)
        return render_template('weather.html', prediction=prediction)
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)