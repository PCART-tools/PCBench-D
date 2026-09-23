def is_multislice_gce_env():
  return is_gce_env() and get_tpu_env_value('MEGASCALE_COORDINATOR_ADDRESS') is not None
