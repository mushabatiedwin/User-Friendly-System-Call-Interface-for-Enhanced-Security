import requests

API_URL = "http://127.0.0.1:8000"


def get_token(username, password):
    response = requests.post(f"{API_URL}/login", data={"username": username, "password": password})

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Login failed! Check username/password.")
        print("Error:", response.json())  # Debugging info
        return None


def execute_command(token, command):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/execute", json={"command": command}, headers=headers)
    return response.json()


if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")

    token = get_token(username, password)

    if not token:
        print("Login failed!")
    else:
        print("Login successful! Your token:", token)
