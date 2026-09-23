def initialize(coordinator_address: Optional[str] = None,
               num_processes: Optional[int] = None,
               process_id: Optional[int] = None):
  """Initialize distributed system for topology discovery.

  Currently, calling ``initialize`` sets up the multi-host GPU backend and Cloud
  TPU backend.

  If you are on GPU platform, you will have to provide the coordinator_address
  and other args to the `initialize` API.

  If you are on TPU platform, the coordinator_address and other args will be
  auto detected but you have the option to provide it too.

  Args:
    coordinator_address: IP address and port of the coordinator. The choice of
      port does not matter, so long as the port is available on the coordinator
      and all processes agree on the port.
      Can be None only for TPU platform. If coordinator_address is None on TPU,
      then it will be auto detected.
    num_processes: Number of processes. Can be None only for TPU platform and
      if None will be determined from the TPU slice metadata.
    process_id: Id of the current process. Can be None only for TPU platform and
      if None will default to the current TPU worker id determined via the TPU
      slice metadata.

  Raises:
    RuntimeError: If `distributed.initialize` is called more than once.

  Example:

  Suppose there are two GPU hosts, and host 0 is the designated coordinator
  with address ``10.0.0.1:1234``. To initialize the GPU cluster, run the
  following commands before anything else.

  On host 0:

  >>> jax.distributed.initialize('10.0.0.1:1234', 2, 0)  # doctest: +SKIP

  On host 1:

  >>> jax.distributed.initialize('10.0.0.1:1234', 2, 1)  # doctest: +SKIP
  """
  global_state.initialize(coordinator_address, num_processes, process_id)
  atexit.register(shutdown)
