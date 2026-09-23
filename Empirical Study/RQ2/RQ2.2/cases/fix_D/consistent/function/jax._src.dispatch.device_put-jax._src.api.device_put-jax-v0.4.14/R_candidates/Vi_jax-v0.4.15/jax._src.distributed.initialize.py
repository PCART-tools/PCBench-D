def initialize(coordinator_address: Optional[str] = None,
               num_processes: Optional[int] = None,
               process_id: Optional[int] = None,
               local_device_ids: Optional[Union[int, Sequence[int]]] = None,
               initialization_timeout: int = 300):
  """Initializes the JAX distributed system.

  Calling :func:`~jax.distributed.initialize` prepares JAX for execution on
  multi-host GPU and Cloud TPU. :func:`~jax.distributed.initialize` must be
  called before performing any JAX computations.

  The JAX distributed system serves a number of roles:

    * it allows JAX processes to discover each other and share topology information,
    * it performs health checking, ensuring that all processes shut down if any process dies, and
    * it is used for distributed checkpointing.

  If you are using TPU, Slurm, or Open MPI, all arguments are optional: if omitted, they
  will be chosen automatically.

  Otherwise, you must provide the ``coordinator_address``,
  ``num_processes``, and ``process_id`` arguments to :func:`~jax.distributed.initialize`.

  Args:
    coordinator_address: the IP address of process `0` and a port on which that
      process should launch a coordinator service. The choice of
      port does not matter, so long as the port is available on the coordinator
      and all processes agree on the port.
      May be ``None`` only on supported environments, in which case it will be chosen automatically.
      Note that special addresses like ``localhost`` or ``127.0.0.1`` usually mean that the program
      will bind to a local interface and are not suitable when running in a multi-host environment.
    num_processes: Number of processes. May be ``None`` only on supported environments, in
      which case it will be chosen automatically.
    process_id: The ID number of the current process. The ``process_id`` values across
      the cluster must be a dense range ``0``, ``1``, ..., ``num_processes - 1``.
      May be ``None`` only on supported environments; if ``None`` it will be chosen automatically.
    local_device_ids: Restricts the visible devices of the current process to ``local_device_ids``.
      If ``None``, defaults to all local devices being visible to the process except when processes
      are launched via Slurm and Open MPI on GPUs. In that case, it will default to a single device per process.
    initialization_timeout: Time period (in seconds) for which connection will
      be retried. If the initialization takes more than the timeout specified,
      the initialization will error. Defaults to 300 secs i.e. 5 mins.

  Raises:
    RuntimeError: If :func:`~jax.distributed.initialize` is called more than once.

  Example:

  Suppose there are two GPU processs, and process 0 is the designated coordinator
  with address ``10.0.0.1:1234``. To initialize the GPU cluster, run the
  following commands before anything else.

  On process 0:

  >>> jax.distributed.initialize(coordinator_address='10.0.0.1:1234', num_processes=2, process_id=0)  # doctest: +SKIP

  On process 1:

  >>> jax.distributed.initialize(coordinator_address='10.0.0.1:1234', num_processes=2, process_id=1)  # doctest: +SKIP
  """
  global_state.initialize(coordinator_address, num_processes, process_id,
                          local_device_ids, initialization_timeout)
  atexit.register(shutdown)
