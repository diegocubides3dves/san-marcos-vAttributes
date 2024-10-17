import os
from vattributes import (hrc_energy, ch_tonnage, chiller_plant_without_hrc_tonnage,
                         cup_chiller_efficiency, cup_cooling_plant_efficiency_part_b,
                         gas_hum_steam, gas_hhw, boiler_hot_water, hw_boiler_eff,
                         hwp_eff, efficiency_equation, stm_boiler_eff)
from dotenv import dotenv_values
from datetime import datetime, timedelta
import requests
from dotenv import dotenv_values

url = os.environ["LOGIN_URL"]
user_info = {"user": os.environ["USER"], "password": os.environ["PASSWORD"]}
headers = {"Content-Type": "application/json"}

# logIn_response= requests.post(f"{url}/3dves/user/logIn", json=user_info, headers=headers)
# token = logIn_response.json().get("token")
# auth_headers = {"Authorization": token, "Content-Type": "application/json"}

def hrc_energy_writing(invoked_by):
  data = hrc_energy([29808, 29812, 29816, 29550, 29554, 29558, 29589, 29593, 29632, 29636])
  now = (datetime.today() + timedelta(hours=0)).isoformat()
  value = {"currentValue": data, "currentDate": now}
  response = requests.put(f"{url}/attributes/29887", json=value)
  if (response.status_code == 200):
    print(f"atributo: 29887, data: {value}, {invoked_by}")
  else:
    print("error escribiendo atributo: 29887")

def writing_ids(ids):
  #[ 173, 183, 184, 30568, 190, 193, 194, 195, 139, 140, 199, 200, 201, 202, 203, 204, 206, 207, 208, 209, 30582, 30569] 30583, 30584, 30585
  data = []

  # 1. agregar los areglos que actualmente estan como argumentos, al campor args que le correponda a cada uno de estos registros en la base de datos.
  data.append(ch_tonnage([29527,29563, 29528, 29526]))#173 is a vAttribute, as virtual attribute is able to have type: "ch_tonnage", args: [29527,29563, 29528, 29526] 
  data.append(ch_tonnage([29533,29563, 29534, 29532]))#183
  data.append(ch_tonnage([29541,29563, 29537, 29539]))#184
  data.append(ch_tonnage([29938,29940, 29937, 29936]))#30568
  calculated_190 = chiller_plant_without_hrc_tonnage([29566, 29563, 29567, 29526, 29532, 29539])
  data.append(calculated_190)#190
  data.append(efficiency_equation([163], [30880]))#193
  data.append(efficiency_equation([163, 153, 254, 182], [30879]))#194
  cup_cooling_plant_efficiency_without_hrc = efficiency_equation([163,255,182], [30880])#195
  data.append(cup_cooling_plant_efficiency_without_hrc)#
  data.append(gas_hum_steam([30922, 30923, 138]))#139
  calculated_140 = gas_hhw([ 30768, 30769, 30770])#29729, 29731, 29733, 29735, 29737,
  data.append(float(calculated_140))#140
  data.append(boiler_hot_water([29625, 29626, 29563]))#199
  data.append(boiler_hot_water([29682, 29683, 29681]))#200
  data.append(boiler_hot_water([29684, 29685, 30358]))#201
  data.append(boiler_hot_water([29686, 29687, 30359]))#202
  calculated_203 = boiler_hot_water([29703, 29704, 29701])
  data.append(calculated_203)#203
  calculated_204 = boiler_hot_water([29700, 29708, 29845])
  data.append(calculated_204)#204
  data.append(hw_boiler_eff([29680,29649,29654, 30768, 30769, 30770])) #206
  data.append(stm_boiler_eff([196, 29704, 29845, 138]))#207 
  data.append(hwp_eff([float(calculated_204), float(calculated_140), 256]))#208 #256 should be in k Watts sol: 256 from 394
  data.append(hwp_eff([float(calculated_203), float(calculated_140), 257]))#209 #257 should be in k Watts sol: 257 from 395
  data.append(boiler_hot_water([29981, 29980, 29982]))#30582 is missing 30583, 30584, 30585
  data.append(ch_tonnage([29984, 29985, 29979, 29984])) #30569

  data.append(boiler_hot_water([30608, 30640,30639]))#30583
  data.append(boiler_hot_water([29897, 30642, 30641]))#30584
  data.append(boiler_hot_water([30195, 30644, 30643]))#30585
  #data.append(boiler_hot_water([30195, 30644, 30643]))#30585 DHW for hospital
  now = (datetime.today() + timedelta(hours=0)).isoformat()
  for i in range(len(data)):
    value = {"currentValue": data[i], "currentDate": now}
    response = requests.put(
      f"{url}/attributes/{ids[i]}",
      json=value)
    if (response.status_code == 200):
      print(f"atributo: {ids[i]}, valor: {value}, ")
    else:
      print(f"error escribiendo atributo: {ids[i]}")