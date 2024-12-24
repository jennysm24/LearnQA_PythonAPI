import requests
import json
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
#params={"token": })
response = requests.get(url)
print(f"Status of task is {response.status_code}")
#print(f"'{response.text}'")
#print(type(response.text))
obj = json.loads(response.text)
token_value = obj["token"]
seconds_value = obj["seconds"]
print(f"Token is {token_value}")
print(f"Seconds is {seconds_value}")
time.sleep(seconds_value)
url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url, params={"token": token_value})
print(f"Status of task is {response.status_code}")
print(f"Status of task is {response.text}")
obj2 = json.loads(response.text)
status_value = obj2["status"]
if response.status_code == 200:
    if status_value == "Job is ready":
        print("The task is really ready")
    elif status_value == "Job is NOT ready":
        print("The task is actually not ready, need to wait")
else:
    print("The status is not 200, try again")




