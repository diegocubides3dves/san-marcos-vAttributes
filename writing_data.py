from vattributes import hrc_energy, ch_tonnage, chiller_plant_without_hrc_tonnage, cup_chiller_efficiency, cup_cooling_plant_efficiency_part_b, gas_hum_steam, gas_hhw, boiler_hot_water, hw_boiler_eff, hwp_eff
from dotenv import dotenv_values
from datetime import datetime, timedelta
import requests

env = dotenv_values(".env")

url = env["LOGIN_URL"]
user_info = {"user": env["USER"], "password": env["PASSWORD"]}
headers = {"Content-Type": "application/json"}

logIn_response= requests.post(f"{url}/3dves/user/logIn", json=user_info, headers=headers)
token = logIn_response.json().get("token")
auth_headers = {"Authorization": token, "Content-Type": "application/json"}

def hrc_energy_writing(invoked_by):
  data = hrc_energy([29808, 29812, 29816, 29550, 29554, 29558, 29589, 29593, 29632, 29636])
  now = (datetime.today() + timedelta(hours=0)).isoformat()
  value = {"currentValue": data, "currentDate": now}
  response = requests.put(f"{url}/3dves/attributes/29887", json=value, headers= auth_headers)
  if (response.status_code == 200):
    print(f"atributo: 29887, data: {value}, {invoked_by}")
  else:
    print("error escribiendo atributo: 29887")

def writing_ids(ids):
  data = []
  data.append(ch_tonnage([29527,29563, 29528, 29526]))
  data.append(ch_tonnage([29533,29563, 29534, 29532]))
  data.append(ch_tonnage([29541,29563, 29537, 29539]))
  data.append(ch_tonnage([29938,29940, 29937, 29936]))
  data.append(chiller_plant_without_hrc_tonnage([29566, 29563, 29567, 29526, 29532, 29539]))
  data.append(cup_chiller_efficiency([150, 151, 152, 190]))
  cup_cooling_plant_efficiency_without_hrc = cup_chiller_efficiency([150, 151, 152, 190]) + cup_cooling_plant_efficiency_part_b([255, 182, 190])
  data.append(cup_cooling_plant_efficiency_without_hrc)
  data.append(gas_hum_steam([30197, 29742, 29932]))
  data.append(gas_hhw([29729, 29731, 29733, 29735, 29737, 29691, 29693, 29695]))
  data.append(boiler_hot_water([29625, 29626, 29563]))
  data.append(boiler_hot_water([29682, 29683, 29681]))
  data.append(boiler_hot_water([29684, 29685, 30358]))
  data.append(boiler_hot_water([29686, 29687, 30359]))
  data.append(boiler_hot_water([29703, 29704, 29701]))
  data.append(boiler_hot_water([29700, 29708, 29845]))
  data.append(hw_boiler_eff([247, 248, 249, 140]))
  data.append(hwp_eff([204, 140, 256]))
  data.append(hwp_eff([203, 140, 257]))
  data.append(boiler_hot_water([29981, 29980, 29882]))
  data.append(ch_tonnage([29984, 29985, 29979, 29984]))

  now = (datetime.today() + timedelta(hours=0)).isoformat()
  for i in range(len(data)):
    value = {"currentValue": data[i], "currentDate": now}
    response = requests.put(f"{url}/3dves/attributes/{ids[i]}", json=value, headers= auth_headers)
    if (response.status_code == 200):
      print(f"atributo: {ids[i]}, valor: {value}, ")
    else:
      print(f"error escribiendo atributo: {ids[i]}")