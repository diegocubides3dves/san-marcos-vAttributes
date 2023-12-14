from writing_data import hrc_energy_writing, writing_ids

def handler(event, context):
  hrc_energy_writing(context)
  outcoming_ids = event.get("ids_to_write")
  writing_ids(outcoming_ids)