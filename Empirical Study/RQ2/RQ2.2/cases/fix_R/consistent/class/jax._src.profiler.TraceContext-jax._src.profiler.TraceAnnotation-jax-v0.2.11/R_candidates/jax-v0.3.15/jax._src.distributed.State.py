class State:
  process_id: int = 0
  service: Optional[Any] = None
  client: Optional[Any] = None
  preemption_sync_manager: Optional[Any] = None

  def initialize(self,
                 coordinator_address: Optional[str] = None,
                 num_processes: Optional[int] = None,
                 process_id: Optional[int] = None):
    coordinator_address = (coordinator_address or
                           os.environ.get('JAX_COORDINATOR_ADDRESS', None))

    if cloud_tpu_init.running_in_cloud_tpu_vm:
      worker_endpoints = cloud_tpu_init.get_metadata(
          'worker-network-endpoints').split(',')
      if coordinator_address is None:
        coordinator_address = worker_endpoints[0].split(':')[2] + ':8476'
      if num_processes is None:
        num_processes = xla_bridge.process_count()
      if process_id is None:
        process_id = int(cloud_tpu_init.get_metadata('agent-worker-number'))

      if num_processes != len(worker_endpoints):
        raise RuntimeError('Number of workers does not equal the number of '
                           'processes. Auto detecting process_id is not possible.'
                           'Please pass process_id manually.')

    if coordinator_address is None:
      raise ValueError('coordinator_address should be defined.')
    if num_processes is None:
      raise ValueError('Number of processes must be defined.')
    if process_id is None:
      raise ValueError('The process id of the current process must be defined.')

    self.process_id = process_id

    if process_id == 0:
      if self.service is not None:
        raise RuntimeError('distributed.initialize should only be called once.')
      logging.info('Starting JAX distributed service on %s', coordinator_address)
      self.service = xla_extension.get_distributed_runtime_service(
          coordinator_address, num_processes, config.jax_coordination_service)

    if self.client is not None:
      raise RuntimeError('distributed.initialize should only be called once.')

    self.client = xla_extension.get_distributed_runtime_client(
        coordinator_address, process_id, config.jax_coordination_service)
    logging.info('Connecting to JAX distributed service on %s', coordinator_address)
    self.client.connect()

    if xla_client._version >= 77 and config.jax_coordination_service:
      self.initialize_preemption_sync_manager()

  def shutdown(self):
    if self.client:
      self.client.shutdown()
      self.client = None
    if self.service:
      self.service.shutdown()
      self.service = None

  def initialize_preemption_sync_manager(self):
    if self.preemption_sync_manager is not None:
      raise RuntimeError(
          'Preemption sync manager should only be initialized once.')
    self.preemption_sync_manager = (
        xla_extension.create_preemption_sync_manager())
    self.preemption_sync_manager.initialize(self.client)
