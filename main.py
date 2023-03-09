import requests
from datetime import datetime
import pytz
import json
from requests.auth import HTTPDigestAuth
import os

GENDER = 'male'
WEIGHT_KG = 61.3
HEIGHT_CM = 234
AGE = 23

API_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"] 
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me what exercise you did: ")

header = {
  "x-app-id": API_ID,
  "x-app-key": API_KEY,
  "x-remote-user-id": "0",
  "Content-Type": "application/json"
}

ex_params = {
   "query": exercise_text,
   "gender": GENDER,
   "weight_kg": WEIGHT_KG,
   "height_cm": HEIGHT_CM,
   "age": AGE,
  }

# nutritionix
exercise_response = requests.post(exercise_endpoint, json=ex_params, headers=header)
exercise = exercise_response.json()
# print(exercise)


USERNAME = os.environ["USERNAME"]
PROJECT_NAME = "myWorkouts"
SHEET_NAME = "workout"
sheety_endpoint = f"https://api.sheety.co/{USERNAME}/{PROJECT_NAME}/{SHEET_NAME}"
# end point is good
# had to make sheet name "workout" instead of "workouts" ? even though it matched?

today = datetime.now().astimezone(pytz.timezone('US/Eastern'))
date = today.strftime("%d/%m/%y")
time = today.strftime("%H:%M:%S")

# use fo rloop so you can include multiple exercises entered at once
for exercise in exercise["exercises"]:
  sheety_params = {
    SHEET_NAME: {  
      "date": date,
      "time": time,
      "exercise": exercise["name"],
      "duration": exercise["duration_min"],
      "calories": exercise["nf_calories"],
      }
    }
  # header = {
  #   "Authorization",
  #   "Basic bnVsbDpudWxs"
  # }

  sheety_response = requests.post(url=sheety_endpoint,
                                  json=sheety_params,
                                  auth=HTTPDigestAuth('jcarbolynn', os.environ['TOKEN']))
  # print(sheety_response.text)



  
  
# time = exercise["exercises"][0]["duration_min"]
# calories = exercise["exercises"][0]["nf_calories"]
# exercise_type = exercise["exercises"][0]["name"]
#
# sheety_params = {
#   SHEET_NAME: {  
#     "date": today.strftime("%d/%m/%y"),
#     "time": today.strftime("%H:%M:%S"),
#     "exercise": exercise_type,
#     "duration": time,
#     "calories": calories}
# }


