import requests

username = "Sreecharan1234"
url = f"https://api.github.com/users/{username}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(type(data))
    print(data['login'],
                data['html_url'],
                data['public_repos'],
                data['followers'],
                data['following'])
else:
    print("Error fetching data:", response.text)