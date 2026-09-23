  @classmethod
  def get_coordinator_address(cls, timeout_secs: int | None) -> str:
    if has_megascale_address():
      # For both GCE via QueuedResources and GKE via JobSet, the
      # Megascale coordinator address is set as the host with process id = 0,
      # so can be used as the jax distributed system coordinator.
      coordinator_address = get_tpu_env_value('MEGASCALE_COORDINATOR_ADDRESS')
    else:
      # For both GCE (QueuedResources and TPUVM create) and GKE via Job API,
      # the workers lists are sorted by process ID so the first one can
      # be used as the jax distributed system coordinator.
      coordinator_address = cls._get_worker_list_in_slice()[0]
    coordinator_address = coordinator_address.split(':')[0]
    logger.debug("TPU Cluster using coordinator address: %s", coordinator_address)
    cls.wait_for_coordinator(coordinator_address, timeout_secs)
    return f'{coordinator_address}:{coordinator_port}'
