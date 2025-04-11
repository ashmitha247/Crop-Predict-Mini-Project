from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import joblib
import requests
import numpy as np
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the trained model
model = joblib.load('model_rf.pkl')

# ThingSpeak channel details
THINGSPEAK_API_KEY = 'PWX6Z0ZH2CQXFG3X'
THINGSPEAK_CHANNEL_ID = '2546193'

# Initialize database
DATABASE = 'predictions.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL,
                        mobile TEXT NOT NULL,
                        address TEXT,
                        state TEXT,
                        pincode TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS predictions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        temperature REAL,
                        humidity REAL,
                        rainfall REAL,
                        wind_speed REAL,
                        crop_suitability TEXT,
                        accuracy REAL,
                        timestamp TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobile = request.form['mobile']
        address = request.form['address']
        state = request.form['state']
        pincode = request.form['pincode']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO users (username, password, email, mobile, address, state, pincode) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (username, password, email, mobile, address, state, pincode))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return 'Username already exists!'
    return render_template('register.html')

init_db()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials!'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        # Extract data from POST request
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        rainfall = float(request.form['rainfall'])
        wind_speed = float(request.form['wind_speed'])

        # Perform prediction
        input_features = np.array([[temperature, humidity, rainfall, wind_speed]])
        prediction = model.predict(input_features)[0]

        # Assuming accuracy is available
        accuracy = 97.0  # Replace with actual accuracy logic if applicable

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save prediction to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO predictions (user_id, temperature, humidity, rainfall, wind_speed, crop_suitability, accuracy, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (session['user_id'], temperature, humidity, rainfall, wind_speed, prediction, accuracy, timestamp))
        conn.commit()
        conn.close()

        # Return prediction result
        return jsonify({'crop_suitability': prediction, 'accuracy': accuracy, 'timestamp': timestamp})
    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/history', methods=['GET', 'POST'])
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Fetch predictions for the logged-in user
    cursor.execute("SELECT id, temperature, humidity, rainfall, wind_speed, crop_suitability, accuracy, timestamp FROM predictions WHERE user_id = ?", (session['user_id'],))
    predictions = cursor.fetchall()
    conn.close()
    
    return render_template('history.html', predictions=predictions)

@app.route('/delete_prediction/<int:prediction_id>', methods=['POST'])
def delete_prediction(prediction_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Delete the prediction with the given ID
        cursor.execute("DELETE FROM predictions WHERE id = ? AND user_id = ?", (prediction_id, session['user_id']))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/update', methods=['GET'])
def update():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        # Fetch data from ThingSpeak
        response = requests.get(f'https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?results=1')
        data = response.json()

        temperature = float(data['feeds'][0]['field1'])
        humidity = float(data['feeds'][0]['field2'])
        rainfall = float(data['feeds'][0]['field3'])
        wind_speed = float(data['feeds'][0]['field4'])

        return jsonify({'temperature': temperature, 'humidity': humidity, 'rainfall': rainfall, 'wind_speed': wind_speed})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
