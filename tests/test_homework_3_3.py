import requests
import pytest


class TestUserAuth:
    expected_values = [
        "HomeWork=hw_value",  # correct value
        "HomeWork=hw_value1",  # wrong value
        ""  # empty value
    ]

    @pytest.mark.parametrize('expected_value', expected_values)
    @pytest.mark.xfail(reason="Test with wrong or empty header value is expected to fail")
    def test_auth_user(self, expected_value):
        data = {'email': 'vinkotov@example.com',
                'password': '1234'}

        url = "https://playground.learnqa.ru/api/homework_cookie"

        response = requests.get(url, params=data)
        for headers_name, headers_value in response.headers.items():
            print(f"Headers name, {headers_name}, Cookie value: {headers_value}")
        assert "Set-Cookie" in response.headers, "There is no Set-Cookie headers in the response"
        # to cut the remaining of the header as the info there is not static, using split method to cut the string by ; symbols
        cookie_value = response.headers['Set-Cookie'].split(';')[0]
        assert cookie_value == expected_value, "Actual value of headers in the response is not correct"
