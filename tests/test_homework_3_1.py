import allure
import pytest


@pytest.mark.skip(reason="This test is skipped as it requires manual actions")
@allure.link("https://software-testing.ru/lms/mod/assign/view.php?id=462959")
class TestLength:
    def test_length(self):
        phrase = input("Set a phrase: ")
        length_phrase = len(phrase)
        assert length_phrase > 0, "No phrase was entered. The input cannot be empty."
        assert length_phrase < 15, f"The length is {length_phrase}, but should be less than 15 "
