import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Cases for PUT request")
@allure.link("https://software-testing.ru/lms/mod/assign/view.php?id=462978")
class TestUserEdit(BaseCase):
    @allure.tag("smoke", "regression")
    @allure.link("https://software-testing.ru/lms/mod/assign/view.php?id=462978")
    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        url = "https://playground.learnqa.ru/api/user/"
        # response1 = requests.post(url, data=register_data)
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
        url2 = "https://playground.learnqa.ru/api/user/login"
        # response2 = requests.post(url2, data=login_data)
        response2 = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        url3 = f"https://playground.learnqa.ru/api/user/{user_id}"
        # response3 = requests.put(url3,
        #                          headers={"x-csrf-token":token},
        #                          cookies={"auth_sid": auth_sid},
        #                          data={"firstName": new_name}
        #                          )
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )
        Assertions.assert_code_status(response3, 200)

        # GET
        url4 = f"https://playground.learnqa.ru/api/user/{user_id}"
        # response4 = requests.get(url4,
        #                          headers={"x-csrf-token": token},
        #                          cookies={"auth_sid": auth_sid}
        #                          )
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        Assertions.assert_json_value_by_name(response4,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit"
                                             )
