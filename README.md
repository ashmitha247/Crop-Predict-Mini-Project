# Crop Suitability Prediction System

## Introduction

Agriculture is the backbone of many economies, and farmers constantly face the challenge of choosing the right crop for their land and climatic conditions. The **Crop Suitability Prediction System** leverages real-time environmental data and machine learning to provide accurate crop recommendations.

By integrating IoT, data science, and AI, this project simulates a smart, data-driven solution for modern agricultural challenges:  
- **Live sensor inputs:** Temperature, humidity, water level, and wind speed  
- **Cloud-based IoT platform:** ThingSpeak  
- **Web dashboard:** Python Flask application  
- **Machine Learning model:** Predicts the best crop for current conditions

---

## Project Objective

- Collect real-time environmental data using sensors
- Send data to a cloud-based IoT platform (ThingSpeak)
- Fetch data into a Python-based Flask web application
- Run a machine learning model trained on real-world agricultural datasets
- Predict the best crop based on live environmental data

---

## System Architecture

**Step-by-step Flow:**

1. **Sensors collect data:** Temperature, Humidity, Water Level, Wind Speed
2. **Arduino reads sensor values** and processes the data
3. **ESP8266 Wi-Fi module sends data** to ThingSpeak (IoT cloud)
4. **Flask application retrieves data** from ThingSpeak
5. **ML Model processes data** and predicts the best crop
6. **Results displayed on web dashboard** for farmers

```
[Sensors] ---> [Microcontroller] ---> [ThingSpeak Cloud]
                                     |
                                     v
                            [Flask Backend]
                          /                \
               [ML Model Predicts]        [API Sends JSON]
                          \                /
                        [Frontend Displays Crop]
```

---

## Hardware Components

- **DHT11 Sensor:** Measures air temperature and humidity  
- **Soil Moisture Sensor:** Measures water level in the field  
- **Wind Speed Sensor:** Measures wind speed in the farming area  
- **Arduino Board:** Reads sensor values and communicates with ESP8266
- **ESP8266 Wi-Fi Module:** Sends sensor data to ThingSpeak cloud

---

## Data Collection & Transmission

- Sensors are connected to an Arduino microcontroller
- The Arduino processes analog/digital input from the sensors
- ESP8266 Wi-Fi module sends this data to ThingSpeak (IoT cloud) using HTTP REST API

---

## Data Storage & IoT Platform

- **ThingSpeak**: Used to store, visualize, and analyze sensor data remotely
- Data is sent as time-series via REST API

---

## Data Retrieval & Processing (Software)

### Flask Web Application

- Built using Python Flask
- Retrieves latest sensor data from ThingSpeak
- Passes live data to the ML model for crop prediction
- Displays the prediction and history in a user-friendly dashboard

### Features

- User Registration and Login
- Real-time crop prediction
- Prediction history and deletion
- Data update from ThingSpeak

---

## Machine Learning Model

- **Data source:** Real-world agricultural datasets (Kaggle)
- **Features used:** Temperature, Humidity, Rainfall, Wind Speed
- **Algorithms:** Random Forest, Decision Trees
- **Training:** Model is trained on historical data and saved as `model_rf.pkl`
- **Accuracy:** ~97% (can be adjusted based on model evaluation)

---

## Project Structure

```
Crop-Predict-Mini-Project/
├── hardware/                 # Arduino & sensor code
│   └── crop_monitor.ino
├── ml/                       # Machine learning model training
│   ├── train_model.ipynb
│   ├── model_rf.pkl
│   └── Crop_recommendation.csv
├── app/                      # Flask web app
│   ├── app.py
│   ├── predictions.db
│   ├── templates/
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── history.html
│   └── static/
│       └── (css/js files)
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Hardware

1. Connect DHT11, soil moisture, and wind speed sensors to the Arduino as per the schematic.
2. Upload the Arduino code (`hardware/crop_monitor.ino`).
3. Configure ESP8266 with Wi-Fi credentials and ThingSpeak channel details.

### Software

1. Clone this repository:
    ```sh
    git clone https://github.com/ashmitha247/Crop-Predict-Mini-Project.git
    cd Crop-Predict-Mini-Project/app
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Download or ensure the ML model file `model_rf.pkl` is present in the app directory.  
   If you want to retrain the model, run the Jupyter notebook in `ml/train_model.ipynb`.

4. Update ThingSpeak API key and channel ID in `app.py` if needed.

5. Run the Flask app:
    ```sh
    python app.py
    ```
6. Open `http://127.0.0.1:5000` in your browser.

---

## Usage

1. Register and log in to the web dashboard.
2. Click "Update" to fetch the latest sensor values from ThingSpeak.
3. View the recommended crop for your current field conditions.
4. Access prediction history for your account.

---

## Requirements

- Python 3.7+
- Flask, joblib, requests, numpy, pandas, scikit-learn, matplotlib, seaborn
- Arduino IDE (for hardware code)
- Sensors: DHT11, soil moisture, wind speed
- ESP8266 Wi-Fi module
- ThingSpeak account

---

## Datasets

- [Kaggle Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)

---



## Acknowledgements

- [ThingSpeak IoT Platform](https://thingspeak.com/)
- [Kaggle Datasets](https://www.kaggle.com/)
- Open-source libraries and the wider Python, Arduino, and ML communities.

