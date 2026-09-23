def is_gke_env():
  return os.environ.get("TPU_WORKER_HOSTNAMES", None) is not None
