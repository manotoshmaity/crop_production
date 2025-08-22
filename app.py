import streamlit as st
import requests

# -----------------------------
# Your IBM Cloud credentials
# -----------------------------
API_KEY = "knv3K2iSf19SDTtkY6gqSlXRbEmm2dA4fRXIhOsA6RuJ"   # Replace with your real API key
DEPLOYMENT_URL = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/crop123/predictions?version=2021-05-01"


# -----------------------------
# Function to get IAM Token
# -----------------------------
def get_iam_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    data = {
        "apikey": api_key,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers)

    if response.status_code != 200:
        st.error(f"Failed to get IAM token: {response.text}")
        return None

    return response.json().get("access_token")


# -----------------------------
# Function to make prediction
# -----------------------------
def predict_crop(N, P, K, temperature, humidity, ph, rainfall):
    token = get_iam_token(API_KEY)
    if token is None:
        return "Authentication failed. Please check API key."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "input_data": [{
            "fields": ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"],
            "values": [[N, P, K, temperature, humidity, ph, rainfall]]
        }]
    }

    response = requests.post(DEPLOYMENT_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Prediction failed: {response.text}"

    result = response.json()
    try:
        return result["predictions"][0]["values"][0][0]
    except Exception as e:
        return f"Unexpected response format: {result}"


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🌱 Crop Prediction App")
st.write("Enter soil & climate values to predict the best crop.")

N = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=50)
P = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=50)
K = st.number_input("Potassium (K)", min_value=0, max_value=200, value=50)
temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0)
humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0)
ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5)
rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=300.0, value=100.0)

if st.button("🌾 Predict Crop"):
    prediction = predict_crop(N, P, K, temperature, humidity, ph, rainfall)
    st.success(f"Predicted Crop: **{prediction}**")