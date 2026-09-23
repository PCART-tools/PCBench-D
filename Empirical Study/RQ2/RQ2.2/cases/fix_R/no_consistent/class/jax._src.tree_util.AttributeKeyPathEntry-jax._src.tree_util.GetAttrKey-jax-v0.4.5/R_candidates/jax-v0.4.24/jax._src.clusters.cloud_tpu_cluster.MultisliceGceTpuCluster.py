class MultisliceGceTpuCluster(clusters.ClusterEnv):
  @classmethod
  def is_env_present(cls) -> bool:
    return running_in_cloud_tpu_vm and is_multislice_gce_env()

  @classmethod
  def get_coordinator_address(cls) -> str:
    coordinator_address = get_tpu_env_value('MEGASCALE_COORDINATOR_ADDRESS')
    coordinator_address = coordinator_address.split(':')[0]

    # The coordinator may not be up before the other hosts try to
    # communicate with it. We check for its existence with retries.
    coordinator_found = False
    lookup_attempt = 1
    max_coordinator_lookups = 50
    while not coordinator_found and lookup_attempt <= max_coordinator_lookups:
      try:
        ip_address = socket.gethostbyname(coordinator_address)
        coordinator_found = True
      except socket.gaierror:
        print(f"Failed to recognize coordinator address {coordinator_address} on attempt {lookup_attempt}, retrying...")
        lookup_attempt += 1
        time.sleep(5)

    if not coordinator_found:
      raise RuntimeError(f"Failed to recognize coordinator address {coordinator_address}")

    # Use a different port for the jax coordinator than the MXLA coordinator,
    # which is set to 8080 in multislice GCE.
    return f'{coordinator_address}:{coordinator_port}'

  @classmethod
  def get_process_count(cls) -> int:
    processes_per_slice = cls._get_process_count_per_slice()
    num_slices = int(get_tpu_env_value('MEGASCALE_NUM_SLICES'))
    return processes_per_slice * num_slices

  @classmethod
  def get_process_id(cls) -> int:
    process_id_in_slice = cls._get_process_id_in_slice()
    slice_id = int(get_tpu_env_value('MEGASCALE_SLICE_ID'))
    processes_per_slice = cls._get_process_count_per_slice()
    return process_id_in_slice + slice_id * processes_per_slice

  @classmethod
  def get_local_process_id(cls) -> int | None:
    return None

  @staticmethod
  def _get_process_count_per_slice() -> int:
    return len(get_gce_worker_endpoints())

  @staticmethod
  def _get_process_id_in_slice() -> int:
    return int(get_metadata('agent-worker-number'))
