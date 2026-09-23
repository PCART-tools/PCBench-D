class SingleSliceGceTpuCluster(clusters.ClusterEnv):
  @classmethod
  def is_env_present(cls) -> bool:
    return running_in_cloud_tpu_vm and is_gce_env() and not is_multislice_gce_env()

  @classmethod
  def get_coordinator_address(cls) -> str:
    return f"{get_gce_worker_endpoints()[0].split(':')[2]}:{coordinator_port}"

  @classmethod
  def get_process_count(cls) -> int:
    return len(get_gce_worker_endpoints())

  @classmethod
  def get_process_id(cls) -> int:
    return int(get_metadata('agent-worker-number'))

  @classmethod
  def get_local_process_id(cls) -> int | None:
    return None
