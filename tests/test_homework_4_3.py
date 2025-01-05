import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

allure.epic("Edit cases")
class TestUserEdit(BaseCase):
    @allure.tag("smoke", "regression")
    @allure.description("this tests successfull edit")
    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {'email': email,
                      'password': password
                      }
        response2 = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        Assertions.assert_json_value_by_name(response4,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit"
                                             )

    # 1
    @allure.tag("negative", "regression")
    @allure.description("this tests edit for user without auth")
    def test_edit_user_without_auth(self):
        # EDIT
        new_name = "Changed Name"
        existing_user_id = 113522
        response = MyRequests.put(f"/user/{existing_user_id}",
                                  data={"firstName": new_name}
                                  )
        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(response, "error", "Auth token not supplied",
                                             f"Expected 'Auth token not supplied', but got {response.text}")

    # 2
    @allure.tag("negative", "regression")
    @allure.description("this tests edit for user with auth of another user")
    def test_edit_user_with_auth_of_different_user(self):
        # EDIT
        new_name = "Changed Name"
        existing_user_id = 113522
        different_user_auth_sid = '838338485e41ae560af15da79127d6afe29c195f2eda777887f675f16e79b704'
        different_user_token = '64ff3c6e73d6e7b18c2abf19a365f8953327179be29c195f2eda777887f675f16e79b704'
        response = MyRequests.put(f"/user/{existing_user_id}",
                                  data={"firstName": new_name},
                                  headers={"x-csrf-token": different_user_token},
                                  cookies={"auth_sid": different_user_auth_sid}
                                  )
        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(response, "error", "This user can only edit their own data.",
                                             f"Expected 'This user can only edit their own data.', but got {response.text}")
        response2 = MyRequests.get(f"/user/{113522}",
                                   headers={"x-csrf-token": different_user_token},
                                   cookies={"auth_sid": different_user_auth_sid}
                                   )
        Assertions.assert_json_has_key(response2, "username")
        actual_username = self.get_json_value(response2, "username")
        expected_username = "learnqa"
        Assertions.assert_json_value_not_expected_by_name(response2, "username", expected_username,
                                                          f"Expected username to be '{expected_username}', but got "
                                                          f"actual value '{actual_username}'")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")

    # 3
    @allure.tag("negative", "regression")
    @allure.description("this tests edit to wrong email")
    def test_edit_user_to_wrong_email(self):
        # EDIT
        new_email = "jennysmmail.ru"
        user_id = 113503
        auth_sid = '838338485e41ae560af15da79127d6afe29c195f2eda777887f675f16e79b704'
        token = '64ff3c6e73d6e7b18c2abf19a365f8953327179be29c195f2eda777887f675f16e79b704'

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email}
                                   )
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Invalid email format",
                                             f"Expected 'Invalid email format', but got {response3.text}")

    # 4
    @allure.tag("negative", "regression")
    @allure.description("this tests edit to short firstname")
    def test_edit_user_to_short_firstname(self):
        # EDIT
        new_firstname = "T"
        user_id = 113503
        auth_sid = '838338485e41ae560af15da79127d6afe29c195f2eda777887f675f16e79b704'
        token = '64ff3c6e73d6e7b18c2abf19a365f8953327179be29c195f2eda777887f675f16e79b704'

        response4 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_firstname}
                                   )
        Assertions.assert_code_status(response4, 400)
        Assertions.assert_json_value_by_name(response4, "error",
                                             "The value for field `firstName` is too short",
                                             f"Expected 'The value for field `firstName` is too short', but got {response4.text}")
