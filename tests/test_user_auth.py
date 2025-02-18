import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        self.url = "https://playground.learnqa.ru/api/user/login"
        self.url2 = "https://playground.learnqa.ru/api/user/auth"
        data = {'email': 'vinkotov@example.com',
                'password': '1234'}
        #response1 = requests.post(self.url, data=data)
        # changed to the method written in a separate lib
        response1 = MyRequests.post('/user/login', data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.description("this test successfully authorize user by email and password")
    @allure.tag('smoke', 'regression')
    def test_auth_user(self):

        # response2 = requests.get(self.url2,
        #   headers={"x-csrf-token": self.token},
        #   cookies={"auth_sid": self.auth_sid})
        # changed to the method written in a separate lib
        response2 = MyRequests.get('/user/auth',
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(response2,
                                             "user_id",
                                             self.user_id_from_auth_method,
                                             f"User id from auth method is not equal id from check method"
                                             )

    @allure.description("this test successfully authorization status w/o sending auth cookie or header")
    @allure.tag('negative', 'regression')
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        # sending either no cookie or no token
        if condition == "no_cookie":
            # changed to the method written in a separate lib
            # response2 = requests.get(self.url2, headers={"x-csrf-token": self.token})
            response2 = MyRequests.get('/user/auth',
                                       headers={"x-csrf-token": self.token})
        else:
            # changed to the method written in a separate lib
            # response2 = requests.get(self.url2, cookies={"auth_sid": self.auth_sid})
            response2 = MyRequests.get('/user/auth',
                                       cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2,
                                             "user_id",
                                             0,
                                             f"User is authorized with condition {condition}"
                                             )
