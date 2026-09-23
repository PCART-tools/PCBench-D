class GkeTpuCluster(MultisliceGceTpuCluster):
  # This class handles both single and multislice GKE as the environment
  # variables are set the same in both cases.
  @classmethod
  def is_env_present(cls) -> bool:
    return running_in_cloud_tpu_vm and is_gke_env()

  @staticmethod
  def _get_process_count_per_slice() -> int:
    tpu_worker_hostnames = str(os.environ.get('TPU_WORKER_HOSTNAMES', None))
    return len(tpu_worker_hostnames.split(','))

  @staticmethod
  def _get_process_id_in_slice() -> int:
    return int(str(os.environ.get('TPU_WORKER_ID')))
