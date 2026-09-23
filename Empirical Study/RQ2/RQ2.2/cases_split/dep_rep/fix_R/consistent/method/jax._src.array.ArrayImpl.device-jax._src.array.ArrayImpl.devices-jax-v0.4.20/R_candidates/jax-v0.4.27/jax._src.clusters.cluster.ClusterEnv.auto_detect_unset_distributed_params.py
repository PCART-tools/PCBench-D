  @classmethod
  # pytype: disable=bad-return-type
  def auto_detect_unset_distributed_params(cls,
                                           coordinator_address: str | None,
                                           num_processes: int | None,
                                           process_id: int | None,
                                           local_device_ids: Sequence[int] | None,
                                           initialization_timeout: int | None,
                                          ) -> tuple[str | None, int | None, int | None,
                                                     Sequence[int] | None]:
    if all(p is not None for p in (coordinator_address, num_processes,
      process_id, local_device_ids)):
      return (coordinator_address, num_processes, process_id,
              local_device_ids)
    env = next((env for env in cls._cluster_types if env.is_env_present()), None)
    if env:
      logger.debug('Initializing distributed JAX environment via %s', env.__name__)
      if coordinator_address is None:
        coordinator_address = env.get_coordinator_address(timeout_secs=initialization_timeout)
      if num_processes is None:
        num_processes = env.get_process_count()
      if process_id is None:
        process_id = env.get_process_id()
      # Never automatically set local_device_ids on TPUs
      # Defaults to single process per device if local_process_id is available.
      # This only runs if we're in a managed distributed environment.
      # Otherwise local_device_ids will remain unset,
      # which will default to all devices being visible.
      if (local_device_ids is None and not running_in_cloud_tpu_vm and
          env.get_local_process_id() is not None):
        local_device_ids = [env.get_local_process_id()] # type: ignore[list-item]
    else:
      logger.debug('Could not find a known environment for initializing distributed JAX. '
        'Known environments: %s', ', '.join(e.__name__ for e in cls._cluster_types))
    return (coordinator_address, num_processes, process_id, local_device_ids)
