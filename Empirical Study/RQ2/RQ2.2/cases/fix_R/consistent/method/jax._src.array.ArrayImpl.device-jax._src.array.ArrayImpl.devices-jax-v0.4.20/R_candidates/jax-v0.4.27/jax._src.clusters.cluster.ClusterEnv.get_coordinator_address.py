  @classmethod
  def get_coordinator_address(cls, timeout_secs: int | None) -> str:
    """Returns address and port used by JAX to bootstrap.

    Process id 0 will open a tcp socket at "hostname:port" where
    all the processes will connect to initialize the distributed JAX service.
    The selected port needs to be free.
    :func:`get_coordinator_address` needs to return the same hostname and port on all the processes.

    Returns:
      "hostname:port"
    """
    raise NotImplementedError("ClusterEnv subclasses must implement get_coordinator_address")
