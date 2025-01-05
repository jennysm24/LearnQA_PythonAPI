from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        id = 2
        #url = f"https://playground.learnqa.ru/api/user/{id}"
        #response = requests.get(url)
        response = MyRequests.get(f"/user/{id}")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        url = "https://playground.learnqa.ru/api/user/login"
        data = {
            'password': '1234',
            'email': 'vinkotov@example.com'
        }

        #response1 = requests.post(url, data=data)
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        #url2 = f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}"
        # response2 = requests.get(url2,
        #                          headers={"x-csrf-token": token},
        #                          cookies={"auth_sid": auth_sid}
        #                          )
        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.assert_json_has_keys(response2, expected_fields)



    def test_get_user_details_auth_as_different_existing_user(self):
        #url = "https://playground.learnqa.ru/api/user/login"
        data = {
            'password': '1234',
            'email': 'vinkotov@example.com'
        }

        # response1 = requests.post(url, data=data)
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        existing_user_id = 113500
        #url2 = f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}"
        # response2 = requests.get(url2,
        #                          headers={"x-csrf-token": token},
        #                          cookies={"auth_sid": auth_sid}
        #                          )
        response2 = MyRequests.get(f"/user/{existing_user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")




