  @classmethod
  def is_env_present(cls) -> bool:
    if not running_in_cloud_tpu_vm:
      logger.debug("Did not detect cloud TPU VM")
      return False
    metadata_response, metadata_code = get_metadata('agent-worker-number')
    if metadata_code == metadata_response_code_success:
      logger.debug("Gce Tpu Cluster detected for Jax Distributed System")
      return True
    else:
      logger.debug("Did not detect Gce Tpu Cluster since agent-worker-number is not set in metadata")
      logger.debug("Metadata code: %s", metadata_code)
      logger.debug("Metadata response: %s", metadata_response)
      return False
