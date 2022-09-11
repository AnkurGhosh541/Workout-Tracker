import os
import requests
from datetime import datetime as dt
from dotenv import load_dotenv

load_dotenv()


ID = os.getenv("NUTRIONIX_ID")
KEY = os.getenv("NUTRIONIX_KEY")

query = input("What exercises you did today: ")

nutrionix_endpoint = os.getenv("NUTRIONIX_ENDPOINT")
headers = {
    "x-app-id": ID,
    "x-app-key": KEY,
    "x-remote-user-id": "0"
}

nutrionix_params = {
    "query": query,
    "gender": "male",
    "weight_kg": 72,
    "age": 20
}

nutrionix_response = requests.post(
    url=nutrionix_endpoint,
    json=nutrionix_params,
    headers=headers
).json()
print(nutrionix_response)

sheety_endpoint = os.getenv("SHEETY_ENDPOINT")
sheety_header = {
    "Authorization": os.getenv("SHEETY_AUTH_HEADER")
}

for each_exercise in nutrionix_response["exercises"]:
    date = dt.now().strftime("%d/%m/%Y")
    time = dt.now().strftime("%I:%M:%S %p")
    exercise = each_exercise["name"]
    duration = each_exercise["duration_min"]
    calories = each_exercise["nf_calories"]

    sheety_params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise.title(),
            "duration(min)": duration,
            "calories": calories,
        }
    }

    sheet_response = requests.post(
        url=sheety_endpoint,
        json=sheety_params,
        headers=sheety_header
    )
    print(sheet_response.text)
