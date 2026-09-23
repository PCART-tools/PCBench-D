  def initialize(self,
                 coordinator_address: str | None = None,
                 num_processes: int | None = None,
                 process_id: int | None = None,
                 local_device_ids: int | Sequence[int] | None = None,
                 initialization_timeout: int = 300,
                 coordinator_bind_address: str | None = None):
    coordinator_address = (coordinator_address or
                           os.environ.get('JAX_COORDINATOR_ADDRESS', None))
    if isinstance(local_device_ids, int):
      local_device_ids = [local_device_ids]

    (coordinator_address, num_processes, process_id, local_device_ids) = (
        clusters.ClusterEnv.auto_detect_unset_distributed_params(
            coordinator_address,
            num_processes,
            process_id,
            local_device_ids,
            initialization_timeout,
        )
    )

    if coordinator_address is None:
      raise ValueError('coordinator_address should be defined.')
    if num_processes is None:
      raise ValueError('Number of processes must be defined.')
    if process_id is None:
      raise ValueError('The process id of the current process must be defined.')

    self.coordinator_address = coordinator_address

    # The default value of [::]:port tells the coordinator to bind to all
    # available addresses on the same port as coordinator_address.
    default_coordinator_bind_address = '[::]:' + coordinator_address.rsplit(':', 1)[1]
    coordinator_bind_address = (coordinator_bind_address or
                                os.environ.get('JAX_COORDINATOR_BIND_ADDRESS',
                                               default_coordinator_bind_address))
    if coordinator_bind_address is None:
      raise ValueError('coordinator_bind_address should be defined.')

    if local_device_ids:
      visible_devices = ','.join(str(x) for x in local_device_ids) # type: ignore[union-attr]
      logger.info('JAX distributed initialized with visible devices: %s', visible_devices)
      config.update("jax_cuda_visible_devices", visible_devices)
      config.update("jax_rocm_visible_devices", visible_devices)

    self.process_id = process_id

    if process_id == 0:
      if self.service is not None:
        raise RuntimeError('distributed.initialize should only be called once.')
      logger.info('Starting JAX distributed service on %s', coordinator_address)
      self.service = xla_extension.get_distributed_runtime_service(
          coordinator_bind_address, num_processes)

    self.num_processes = num_processes

    if self.client is not None:
      raise RuntimeError('distributed.initialize should only be called once.')

    self.client = xla_extension.get_distributed_runtime_client(
        coordinator_address, process_id, init_timeout=initialization_timeout)
    logger.info('Connecting to JAX distributed service on %s', coordinator_address)
    self.client.connect()

    self.initialize_preemption_sync_manager()
