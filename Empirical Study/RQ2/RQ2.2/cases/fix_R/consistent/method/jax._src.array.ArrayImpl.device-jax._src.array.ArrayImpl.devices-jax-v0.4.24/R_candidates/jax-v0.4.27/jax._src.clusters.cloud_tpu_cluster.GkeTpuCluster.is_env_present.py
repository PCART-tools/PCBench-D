  @classmethod
  def is_env_present(cls) -> bool:
    if running_in_cloud_tpu_vm and os.environ.get("TPU_WORKER_HOSTNAMES") is not None:
      logger.debug("Gke Tpu Cluster detected for Jax Distributed System")
      return True
    else:
      if not running_in_cloud_tpu_vm:
        logger.debug("Did not detect cloud TPU VM")
      else:
        logger.debug("Did not detect TPU GKE cluster since TPU_WORKER_HOSTNAMES is not set")
      return False
