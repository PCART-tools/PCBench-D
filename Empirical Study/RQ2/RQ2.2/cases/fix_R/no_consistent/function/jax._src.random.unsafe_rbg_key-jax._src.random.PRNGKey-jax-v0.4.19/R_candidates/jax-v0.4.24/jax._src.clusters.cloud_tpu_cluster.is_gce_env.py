def is_gce_env():
  worker_number_string = get_metadata('agent-worker-number')
  try:
    worker_number = int(worker_number_string)
    return True
  except:
    return False
