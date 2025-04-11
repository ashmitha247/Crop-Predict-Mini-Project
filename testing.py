from flask import Flask, render_template, request, jsonify
import joblib
import requests
import numpy as np
# response = requests.get(f'https://api.thingspeak.com/channels/2546193/feeds.json?results=1')
# response = requests.get(f'https://api.thingspeak.com/channels/2546193/feeds.json?results=1')
# data = response.json()

#     # Extract the latest sensor data (assuming your field names in ThingSpeak are 'field1', 'field2', etc.)
# temperature = float(data['feeds'][0]['field1'])
# humidity = float(data['feeds'][0]['field2'])
# rainfall = float(data['feeds'][0]['field3'])
# wind_speed = float(data['feeds'][0]['field4'])
# input_features = np.array([[temperature, humidity, rainfall, wind_speed]])
# print(input_features)


app = Flask(__name__)

# Load the trained model
model = joblib.load('model_rf.pkl')

# ThingSpeak channel details
THINGSPEAK_API_KEY = 'PWX6Z0ZH2CQXFG3X'
THINGSPEAK_CHANNEL_ID = '2546193'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from ThingSpeak or manual inputs
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        rainfall = float(request.form['rainfall'])
        wind_speed = float(request.form['wind_speed'])

        # Predict the crop suitability
        input_features = np.array([[temperature, humidity, rainfall, wind_speed]])
        print(input_features)
        prediction = model.predict(input_features)
        
        # Map prediction to crop class
        # Assuming label_encoder is already used to encode crop types
        crop_suitability = prediction[0]

        return jsonify({'crop_suitability': crop_suitability})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/update', methods=['GET'])
def update_from_thingspeak():
    # Fetch latest data from ThingSpeak
    response = requests.get(f'https://api.thingspeak.com/channels/2546193/feeds.json?results=1')
    data = response.json()

    # Extract the latest sensor data (assuming your field names in ThingSpeak are 'field1', 'field2', etc.)
    temperature = float(data['feeds'][0]['field1'])
    humidity = float(data['feeds'][0]['field2'])
    rainfall = float(data['feeds'][0]['field3'])
    wind_speed = float(data['feeds'][0]['field4'])

    # Use the data for prediction
    input_features = np.array([[temperature, humidity, rainfall, wind_speed]])
    prediction = model.predict(input_features)
    
    # Map prediction to crop class
    crop_suitability = prediction[0]
    
    return jsonify({'temperature': temperature, 'humidity': humidity, 'rainfall': rainfall, 
                    'wind_speed': wind_speed, 'crop_suitability': crop_suitability})

if __name__ == '__main__':
    app.run(debug=True)
