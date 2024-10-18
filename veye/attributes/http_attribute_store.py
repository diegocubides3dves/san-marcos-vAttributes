import os
import requests

url = os.environ["LOGIN_URL"]
user_info = { "user": os.environ["USER"], "password": os.environ["PASSWORD"] }
headers = {"Content-Type": "application/json"}
# logIn_response= requests.post(f"{url}/3dves/user/logIn", json=user_info, headers=headers)
# token = logIn_response.json().get("token")
# auth_headers = {"Authorization": token, "Content-Type": "application/json"}

def get_by_id (id):
  if type(id) == int:
    response = requests.get(f"{url}/attributes/{id}")
    return response.json()
  else:
    return id

def put(id, attribute):
  return requests.put(
    f"{url}/attributes/{id}",
    json=attribute
  )  
