import allure
import requests
import pytest

@allure.epic("Expected results for useк agents with parametrization")
class TestUserAuth:
    user_agents = [
        #passed
        (
            "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}
        ),
        #failed
        (
            "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
            {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}
        ),
        #failed
        (
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}
        ),
        #passed
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
            {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}
        ),
        #failed
        (
            "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
        ),
        #passed
        (
            "",
            {'platform': 'Unknown', 'browser': 'Unknown', 'device': 'Unknown'}
        )
    ]

    @pytest.mark.parametrize("user_agent, expected_result", user_agents)
    @pytest.mark.xfail(reason="Some tests are expected to fail")
    def test_auth_user(self, user_agent, expected_result):
        data = {'email': 'vinkotov@example.com',
                'password': '1234'}

        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

        response = requests.get(url, headers={"User-Agent": user_agent})
        print(response.text)
        result = response.json()
        assert response.status_code == 200, f"The code is expected to be 200, but got {response.status_code}"
        assert result['platform'] == expected_result[
            'platform'], f"Expected platform: {expected_result['platform']}, but got {result['platform']}"
        assert result['browser'] == expected_result[
            'browser'], f"Expected browser: {expected_result['browser']}, but got {result['browser']}"
        assert result['device'] == expected_result[
            'device'], f"Expected device: {expected_result['device']}, but got {result['device']}"
