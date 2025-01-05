import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Cases for Delete request")
class TestUserDelete(BaseCase):
    #1
    def test_delete_some_user_without_auth(self):
        # Register
        id =2
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        #LOGIN
        response = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        #DELETE
        response1 = MyRequests.delete(f"/user/{id}", data=login_data,
                                      headers={"x-csrf-token":token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response1, 400)
        Assertions.assert_json_value_by_name(response1, "error", "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
                                             f"Expected 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', but got {response1.text}")
#2
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("this test the deletion of user")
    @allure.tag('smoke', 'regression')
    def test_delete_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post('/user/', data=register_data)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response2, "id")

        # LOGIN
        login_data = {'email': email,
                      'password': password
                      }
        response3 = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # DELETE
        response4 = MyRequests.delete(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "success",
                                             "!",
                                             f"Expected '!', but got {response4.text}")

        # GET
        response5 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        Assertions.assert_expected_response_text(response5, "User not found",
                                                 f"Expected 'User not found', but got {response5.text}")
#3
    @allure.tag('negative', 'regression')
    def test_delete_just_created_user_with_other_auth(self):
        # Register
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post('/user/', data=register_data)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response2, "id")

        # LOGIN
        login_data = {'email': email,
                      'password': password
                      }
        response3 = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # DELETE
        different_user_auth = "838338485e41ae560af15da79127d6afe29c195f2eda777887f675f16e79b704"
        different_user_token = "64ff3c6e73d6e7b18c2abf19a365f8953327179be29c195f2eda777887f675f16e79b704"
        response4 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": different_user_auth},
                                      cookies={"auth_sid": different_user_token}
                                      )
        Assertions.assert_code_status(response4, 400)
        Assertions.assert_json_value_by_name(response4, "error", "Auth token not supplied",
                                             f"Expected 'Auth token not supplied', but got {response4.text}")

