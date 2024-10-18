from vattributes  import vAttributes
from datetime import datetime, timedelta
from veye.attributes.http_attribute_store import put

virtual_attributes = vAttributes()

def hrc_energy_writing(invoked_by):
  data = virtual_attributes.hrc_energy([29808, 29812, 29816, 29550, 29554, 29558, 29589, 29593, 29632, 29636])
  now = (datetime.today() + timedelta(hours=0)).isoformat()
  value = {"currentValue": data, "currentDate": now}
  
  response = put(29887, value)
  if (response.status_code == 200):
    print(f"atributo: 29887, data: {value}, {invoked_by}")
  else:
    print("error escribiendo atributo: 29887")

def writing_ids(ids):
  #[ 173, 183, 184, 30568, 190, 193, 194, 195, 139, 140, 199, 200, 201, 202, 203, 204, 206, 207, 208, 209, 30582, 30569] 30583, 30584, 30585
  data = []

  # 1. agregar los areglos que actualmente estan como argumentos, al campor args que le correponda a cada uno de estos registros en la base de datos.
  data.append(virtual_attributes.ch_tonnage([29527,29563, 29528, 29526]))#173 is a vAttribute, as virtual attribute is able to have type: "virtual_attributes.ch_tonnage", args: [29527,29563, 29528, 29526] 
  data.append(virtual_attributes.ch_tonnage([29533,29563, 29534, 29532]))#183
  data.append(virtual_attributes.ch_tonnage([29541,29563, 29537, 29539]))#184
  data.append(virtual_attributes.ch_tonnage([29938,29940, 29937, 29936]))#30568
  calculated_190 = virtual_attributes.chiller_plant_without_hrc_tonnage([29566, 29563, 29567, 29526, 29532, 29539])
  data.append(calculated_190)#190
  data.append(virtual_attributes.efficiency_equation([163], [30880]))#193
  data.append(virtual_attributes.efficiency_equation([163, 153, 254, 182], [30879]))#194
  cup_cooling_plant_efficiency_without_hrc = virtual_attributes.efficiency_equation([163,255,182], [30880])#195
  data.append(cup_cooling_plant_efficiency_without_hrc)#
  data.append(virtual_attributes.gas_hum_steam([30922, 30923, 138]))#139
  calculated_140 = virtual_attributes.gas_hhw([ 30768, 30769, 30770])#29729, 29731, 29733, 29735, 29737,
  data.append(float(calculated_140))#140
  data.append(virtual_attributes.boiler_hot_water([29625, 29626, 29563]))#199
  data.append(virtual_attributes.boiler_hot_water([29682, 29683, 29681]))#200
  data.append(virtual_attributes.boiler_hot_water([29684, 29685, 30358]))#201
  data.append(virtual_attributes.boiler_hot_water([29686, 29687, 30359]))#202
  calculated_203 = virtual_attributes.boiler_hot_water([29703, 29704, 29701])
  data.append(calculated_203)#203
  calculated_204 = virtual_attributes.boiler_hot_water([29700, 29708, 29845])
  data.append(calculated_204)#204
  data.append(virtual_attributes.hw_boiler_eff([29680,29649,29654, 30768, 30769, 30770])) #206
  data.append(virtual_attributes.stm_boiler_eff([196, 29704, 29845, 138]))#207 
  data.append(virtual_attributes.hwp_eff([float(calculated_204), float(calculated_140), 256]))#208 #256 should be in k Watts sol: 256 from 394
  data.append(virtual_attributes.hwp_eff([float(calculated_203), float(calculated_140), 257]))#209 #257 should be in k Watts sol: 257 from 395
  data.append(virtual_attributes.boiler_hot_water([29981, 29980, 29982]))#30582 is missing 30583, 30584, 30585
  data.append(virtual_attributes.ch_tonnage([29984, 29985, 29979, 29984])) #30569

  data.append(virtual_attributes.boiler_hot_water([30608, 30640,30639]))#30583
  data.append(virtual_attributes.boiler_hot_water([29897, 30642, 30641]))#30584
  data.append(virtual_attributes.boiler_hot_water([30195, 30644, 30643]))#30585
  #data.append(boiler_hot_water([30195, 30644, 30643]))#30585 DHW for hospital
  now = (datetime.today() + timedelta(hours=0)).isoformat()

  for i in range(len(data)):
    value = {"currentValue": data[i], "currentDate": now}
    response = put(ids[i], value)
    if (response.status_code == 200):
      print(f"atributo: {ids[i]}, valor: {value}, ")
    else:
      print(f"error escribiendo atributo: {ids[i]}")