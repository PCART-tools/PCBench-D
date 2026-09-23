def get_gce_worker_endpoints() -> str:
  return get_metadata('worker-network-endpoints').split(',')
