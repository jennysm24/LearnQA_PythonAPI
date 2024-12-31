import requests
import pytest

class TestUserAuth:
    expected_values = [
        "hw_value",  # correct value
        "hw_value1",  # wrong value
        ""  # empty value
    ]

    @pytest.mark.parametrize('expected_value', expected_values)
    def test_auth_user(self, expected_value):
        data = {'email': 'vinkotov@example.com',
                'password': '1234'}

        url = "https://playground.learnqa.ru/api/homework_cookie"

        response = requests.get(url, params=data)
        for cookie_name, cookie_value in response.cookies.items():
            print(f"Cookie name, {cookie_name}, Cookie value: {cookie_value}")
        assert "HomeWork" in response.cookies, "There is no HomeWork cookie in the response"
        assert cookie_value == expected_value, "Actual value of cookie in the response is not correct"