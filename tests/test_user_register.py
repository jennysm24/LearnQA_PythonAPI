import allure
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Cases for user registration")
class TestUserRegister(BaseCase):
    @allure.tag("smoke", "regression")
    @allure.description("this tests successful registration of user")
    def test_create_user_successfully(self):
        url = "https://playground.learnqa.ru/api/user/"
        data = self.prepare_registration_data()
        #response = requests.post(url, data=data)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.tag("negative", "regression")
    @allure.description("this tests already existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        url = "https://playground.learnqa.ru/api/user/"
        data = self.prepare_registration_data(email)

        #response = requests.post(url, data=data)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"


