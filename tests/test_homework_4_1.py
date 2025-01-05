import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest


class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        # url = "https://playground.learnqa.ru/api/user/"
        data = self.prepare_registration_data()
        # response = requests.post(url, data=data)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        # url = "https://playground.learnqa.ru/api/user/"
        data = self.prepare_registration_data(email)

        # response = requests.post(url, data=data)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    # 1
    def test_create_user_without_at(self):
        email = 'vinkotovexample.com'
        # url = "https://playground.learnqa.ru/api/user/"
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_text(response, "Invalid email format",
                                                 f"Expected 'Invalid email format', but got {response.text}")

    # 2

    required_fields = ["password", "username", "firstName", "lastName", "email"]
    @pytest.mark.parametrize("empty_field", required_fields)
    def test_create_user_without_required_field(self, empty_field):
        data = self.prepare_registration_data()
        data[empty_field] = ""
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_text(response, f"The value of '{empty_field}' field is too short",
                                                 f"Expected 'The value of '{empty_field}' field is too short, but got '{response.text}'")


    # 3
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data(username="T")
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_text(response, "The value of 'username' field is too short",
                                                 f"Expected 'The value of 'username' field is too short', but got {response.text}")

    # 4
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data(username=
                                              "user_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_text(response, "The value of 'username' field is too long",
                                                 f"Expected 'The value of 'username' field is too long', but got {response.text}")
