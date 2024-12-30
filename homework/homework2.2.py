import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
history_of_redirects = []
if response.status_code == 200:
    for i in range( len(response.history)):
        redirect_url = response.history[i].url
        history_of_redirects.append(redirect_url)
    final_redirect = response.url
    print(response.status_code)
    print(f"Redirect history {history_of_redirects}")
    print(f"Count of redirects {len(response.history)-1}")
    print(f"Final redirect to {final_redirect}")
else:
    print(f"Expected status is 200, but got {response.status_code}")
