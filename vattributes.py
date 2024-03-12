from pymongo import MongoClient

client = MongoClient('mongodb://52.36.190.119:27017')
db = client['sanmarcos']
collection = db['attributes']

def attribute_current_value(id):
  if type(id) == int:
    for document in collection.find({"_id": id}):
      value = document['currentValue']
      if str(value).isnumeric():
        return value
      else:
        return -999
  else:
    return id
  
def hrc_energy(ids):
  electric_meter = attribute_current_value(30567)
  result=[]
  for id in ids:
    current_value= float(attribute_current_value(id))
    if (current_value >= 0):
      result.append(current_value)
    else:
      result.append(0)
  return float(electric_meter) - sum(result)

def ch_tonnage(ids):
  supply_flow_id, supply_temp_id, return_temp_id, status_id = ids
  current_supply_flow = float(attribute_current_value(supply_flow_id))
  current_supply_temp = float(attribute_current_value(supply_temp_id))
  current_return_temp = float(attribute_current_value(return_temp_id))
  current_status = float(attribute_current_value(status_id))
  if (current_supply_flow <= 0 or current_supply_temp <= 0 or current_return_temp <= 0 or current_status <= 0):
    return 0
  else:
    return current_supply_flow*(abs(current_return_temp - current_supply_temp))/24
  
def chiller_plant_without_hrc_tonnage(ids):
  supply_flow_id, supply_temp_id, return_temp_id, ch1_status_id, ch2_status_id, ch3_status_id = ids
  current_supply_flow = float(attribute_current_value(supply_flow_id))
  current_supply_temp = float(attribute_current_value(supply_temp_id))
  current_return_temp = float(attribute_current_value(return_temp_id))
  ch1_current_status = float(attribute_current_value(ch1_status_id))
  ch2_current_status = float(attribute_current_value(ch2_status_id))
  ch3_current_status = float(attribute_current_value(ch3_status_id))
  if (current_supply_flow <= 0 or current_supply_temp <= 0 or current_return_temp <= 0 or (ch1_current_status <= 0 and ch2_current_status <= 0 and ch3_current_status <= 0)):
    return 0
  else:
    return current_supply_flow*(abs(current_return_temp - current_supply_temp))/24
  
def cup_chiller_efficiency(ids):
  ch1_energy_id, ch2_energy_id, ch3_energy_id, cup_supply_tonn_id = ids
  current_ch1_energy = float(attribute_current_value(ch1_energy_id))
  current_ch2_energy = float(attribute_current_value(ch2_energy_id))
  current_ch3_energy = float(attribute_current_value(ch3_energy_id))
  current_cup_supply_tonn = float(attribute_current_value(cup_supply_tonn_id))
  if (current_cup_supply_tonn <=0):
    return 0
  else:
    return (current_ch1_energy+current_ch2_energy+current_ch3_energy)/current_cup_supply_tonn
def efficiency_equation(numerator:list, demominator:list):
  numerator_val = sum([float(attribute_current_value(i)) for i in numerator])
  denominator_val = sum([float(attribute_current_value(i)) for i in demominator])
  return numerator_val / denominator_val if round(denominator_val,2) > 0 else 0
def cup_cooling_plant_efficiency_part_b(ids):
  chw_pumps_energy_without_hrc_id, total_heat_reject_energy_id, cup_supply_tonn_id = ids
  current_chw_pumps_energy_without_hrc = float(attribute_current_value(chw_pumps_energy_without_hrc_id))
  current_total_heat_reject_energy = float(attribute_current_value(total_heat_reject_energy_id))
  current_cup_supply_tonn = float(attribute_current_value(cup_supply_tonn_id))
  if (current_cup_supply_tonn <=0):
    return 0
  else:
    return (current_chw_pumps_energy_without_hrc+current_total_heat_reject_energy)/current_cup_supply_tonn
  
def gas_hum_steam(ids):
  stm5_id, stm1_id, ng1_id = ids
  current_stm5 = float(attribute_current_value(stm5_id))
  current_stm1 = float(attribute_current_value(stm1_id))
  current_ng1 = float(attribute_current_value(ng1_id))
  if (current_stm5 <=0 or round(current_stm1, 2) <=0 or current_ng1 <=0):
    return 0
  else:
    return (current_stm5/current_stm1)*current_ng1
  
def gas_hhw(ids):
  result=[]
  for id in ids:
    current_value= float(attribute_current_value(id))
    if (current_value >= 0):
      result.append(current_value)
    else:
      result.append(0)
  return sum(result)

def boiler_hot_water(ids):
  supply_flow_id, supply_temp_id, return_temp_id = ids
  current_supply_flow = float(attribute_current_value(supply_flow_id))
  current_supply_temp = float(attribute_current_value(supply_temp_id))
  current_return_temp = float(attribute_current_value(return_temp_id))
  if (current_supply_flow <=0 or current_supply_temp <=0 or current_return_temp <=0):
    return 0
  else:
    return 5e-4*current_supply_flow*abs(current_supply_temp - current_return_temp)

def hw_boiler_eff(ids):
  hhwb1_flow_id, hhwb2_flow_id, hhwb3_flow_id, gas_used_hhw_id = ids
  current_hhwb1_flow = float(attribute_current_value(hhwb1_flow_id))
  current_hhwb2_flow = float(attribute_current_value(hhwb2_flow_id))
  current_hhwb3_flow = float(attribute_current_value(hhwb3_flow_id))
  current_gas_used_hhw = float(attribute_current_value(gas_used_hhw_id))
  if current_gas_used_hhw <= 0:
    return 0
  else:
    return 3.412*(current_hhwb1_flow + current_hhwb2_flow + current_hhwb3_flow)/(current_gas_used_hhw)
  
def hwp_eff(ids):
  hhw_supply_out_id, gas_used_hhw_id, pumping_energy_id = ids
  current_hhw_supply_out = float(attribute_current_value(hhw_supply_out_id))
  current_gas_used_hhw = float(attribute_current_value(gas_used_hhw_id))
  current_pumping_energy = float(attribute_current_value(pumping_energy_id))
  if (current_gas_used_hhw <=0 or current_pumping_energy <=0):
    return 0
  else:
    return 1e5*current_hhw_supply_out/(current_gas_used_hhw + 3.41214*current_pumping_energy) # Return in percentage 