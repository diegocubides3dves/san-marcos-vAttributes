class vAttributes:
  def __init__(self, attribute_store):
    self.attribute_store = attribute_store
    
  def attribute_current_value(self, id):
    if type(id) != int:
      return id
    
    attribute = self.attribute_store.get_by_id(id)
    value = attribute.get("currentValue") 
    try:
      value = max(0, float(value))
    except:
      pass

    status = attribute.get("status")
    if status == 'out-of-range' or status == 'error':
      return -9999
    elif str(value).isnumeric() or type(value) == int or type(value) == float:
      return value
    else:
      return -9999
    
  def hrc_energy(self, ids):
    electric_meter = self.attribute_current_value(30567)
    if electric_meter < 0: electric_meter = 0
    result=[]
    for id in ids:
      current_value= float(self.attribute_current_value(id))
      if (current_value >= 0):
        result.append(current_value)
      else:
        result.append(0)
    return float(electric_meter) - sum(result)

  def ch_tonnage(self, ids):
    supply_flow_id, supply_temp_id, return_temp_id, status_id = ids
    current_supply_flow = float(self.attribute_current_value(supply_flow_id))
    current_supply_temp = float(self.attribute_current_value(supply_temp_id))
    current_return_temp = float(self.attribute_current_value(return_temp_id))
    current_status = float(self.attribute_current_value(status_id))
    if (current_supply_flow <= 0 or current_supply_temp <= 0 or current_return_temp <= 0 or current_status <= 0):
      return 0
    else:
      return current_supply_flow*(abs(current_return_temp - current_supply_temp))/24
    
  def chiller_plant_without_hrc_tonnage(self, ids):
    supply_flow_id, supply_temp_id, return_temp_id, ch1_status_id, ch2_status_id, ch3_status_id = ids
    current_supply_flow = float(self.attribute_current_value(supply_flow_id))
    current_supply_temp = float(self.attribute_current_value(supply_temp_id))
    current_return_temp = float(self.attribute_current_value(return_temp_id))
    ch1_current_status = float(self.attribute_current_value(ch1_status_id))
    ch2_current_status = float(self.attribute_current_value(ch2_status_id))
    ch3_current_status = float(self.attribute_current_value(ch3_status_id))
    if (current_supply_flow <= 0 or current_supply_temp <= 0 or current_return_temp <= 0 or (ch1_current_status <= 0 and ch2_current_status <= 0 and ch3_current_status <= 0)):
      return 0
    else:
      return current_supply_flow*(abs(current_return_temp - current_supply_temp))/24
    
  def cup_chiller_efficiency(self, ids):
    ch1_energy_id, ch2_energy_id, ch3_energy_id, cup_supply_tonn_id = ids
    current_ch1_energy = float(self.attribute_current_value(ch1_energy_id))
    current_ch2_energy = float(self.attribute_current_value(ch2_energy_id))
    current_ch3_energy = float(self.attribute_current_value(ch3_energy_id))
    current_cup_supply_tonn = float(self.attribute_current_value(cup_supply_tonn_id))
    if (current_cup_supply_tonn <=0):
      return 0
    else:
      return (current_ch1_energy+current_ch2_energy+current_ch3_energy)/current_cup_supply_tonn
  
  def efficiency_equation(self, numerator:list, demominator:list):
    numerator_val = sum([float(self.attribute_current_value(i)) for i in numerator])
    denominator_val = sum([float(self.attribute_current_value(i)) for i in demominator])
    return numerator_val / denominator_val if round(denominator_val,2) > 0 else 0
  
  def cup_cooling_plant_efficiency_part_b(self, ids):
    chw_pumps_energy_without_hrc_id, total_heat_reject_energy_id, cup_supply_tonn_id = ids
    current_chw_pumps_energy_without_hrc = float(self.attribute_current_value(chw_pumps_energy_without_hrc_id))
    current_total_heat_reject_energy = float(self.attribute_current_value(total_heat_reject_energy_id))
    current_cup_supply_tonn = float(self.attribute_current_value(cup_supply_tonn_id))
    if (current_cup_supply_tonn <=0):
      return 0
    else:
      return (current_chw_pumps_energy_without_hrc+current_total_heat_reject_energy)/current_cup_supply_tonn
    
  def gas_hum_steam(self, ids):
    stm5_id, stm1_id, ng1_id = ids
    current_stm5 = float(self.attribute_current_value(stm5_id))
    current_stm1 = float(self.attribute_current_value(stm1_id))
    current_ng1 = float(self.attribute_current_value(ng1_id))
    if (current_stm5 <=0 or round(current_stm1, 2) <=0 or current_ng1 <=0):
      return 0
    else:
      return (current_stm5/current_stm1)*current_ng1
    
  def gas_hhw(self, ids):
    result=[]
    for id in ids:
      current_value= float(self.attribute_current_value(id))
      if (current_value >= 0):
        result.append(current_value)
      else:
        result.append(0)
    return sum(result)

  def boiler_hot_water(self, ids):
    supply_flow_id, supply_temp_id, return_temp_id = ids
    current_supply_flow = float(self.attribute_current_value(supply_flow_id))
    current_supply_temp = float(self.attribute_current_value(supply_temp_id))
    current_return_temp = float(self.attribute_current_value(return_temp_id))
    if (current_supply_flow <=0 or current_supply_temp <=0 or current_return_temp <=0):
      return 0
    else:
      return 5e-4*current_supply_flow*abs(current_supply_temp - current_return_temp)

  def hw_boiler_eff(self, ids):
    hhwb1_flow_id, hhwb2_flow_id, hhwb3_flow_id, gas_used_hhw1_id, gas_used_hhw2_id, gas_used_hhw3_id = ids
    current_hhwb1_flow = float(self.attribute_current_value(hhwb1_flow_id))
    current_hhwb2_flow = float(self.attribute_current_value(hhwb2_flow_id))
    current_hhwb3_flow = float(self.attribute_current_value(hhwb3_flow_id))
    current_gas_used_hhw1 = float(self.attribute_current_value(gas_used_hhw1_id))
    current_gas_used_hhw2 = float(self.attribute_current_value(gas_used_hhw2_id))
    current_gas_used_hhw3 = float(self.attribute_current_value(gas_used_hhw3_id))
    if (current_gas_used_hhw1 + current_gas_used_hhw2 + current_gas_used_hhw3) <= 0:
      return 0
    else:
      return 100000*(current_hhwb1_flow + current_hhwb2_flow + current_hhwb3_flow)/(current_gas_used_hhw1 + current_gas_used_hhw2 + current_gas_used_hhw3)
    
  def stm_boiler_eff(self, ids):
    stm_st2_id, hhws_temp_id, hhwr_temp_id, stm_ng_id = ids
    current_stm_st2 = float(self.attribute_current_value(stm_st2_id))
    current_hhws_temp = float(self.attribute_current_value(hhws_temp_id))
    current_hhwr_temp = float(self.attribute_current_value(hhwr_temp_id))
    current_stm_ng = float(self.attribute_current_value(stm_ng_id))
    if current_stm_ng <= 0:
      return 0.0
    else:
      return 0.1*current_stm_st2*abs(current_hhws_temp - current_hhwr_temp)/current_stm_ng 
    
  def hwp_eff(self, ids):
    hhw_supply_out_id, gas_used_hhw_id, pumping_energy_id = ids
    current_hhw_supply_out = float(self.attribute_current_value(hhw_supply_out_id))
    current_gas_used_hhw = float(self.attribute_current_value(gas_used_hhw_id))
    current_pumping_energy = float(self.attribute_current_value(pumping_energy_id))
    if (current_gas_used_hhw <=0 or current_pumping_energy <=0):
      return 0
    else:
      return 1e5*current_hhw_supply_out/(current_gas_used_hhw + 3.41214*current_pumping_energy) # Return in percentage 
  