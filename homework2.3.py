import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
list_of_methods = ["GET", "POST", "PUT", "DELETE"]
# Question 1
response = requests.get(url)
print(f"For first question status code is {response.status_code}")
print(f"For first question response text is '{response.text}'")
# Question 2
response = requests.head(url)
print(f"For second question status code is {response.status_code}")
print(f"For second question response text is '{response.text}'")
print("Headers:", response.headers)
# Question 3
response = requests.get(url, params={"method": "GET"})
print(f"For third question status code is {response.status_code}")
print(f"For third question response text is '{response.text}'")
# Question 4
for current_method in list_of_methods:
    for method_param_or_data in list_of_methods:
        if current_method == "GET":
            response = requests.get(url, params={"method": method_param_or_data})
        elif current_method == "POST":
            response = requests.post(url, params={"method": method_param_or_data})
        elif current_method == "PUT":
            response = requests.put(url, params={"method": method_param_or_data})
        elif current_method == "DELETE":
            response = requests.delete(url, data={"method": method_param_or_data})
        if current_method != method_param_or_data and response.text != "Wrong method provided":
            print(f"Mismatch between type: {current_method} and method = {method_param_or_data} returned response: {response.text}")
        elif current_method == method_param_or_data and response.text != '{"success":"!"}':
            print(f"Error: Type {current_method} with method={method_param_or_data} did not return success: {response.text}")
