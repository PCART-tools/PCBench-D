  @classmethod
  def get_local_process_id(cls) -> int | None:
    """ Get index of current process inside a host.

    The method is only useful to support single device per process.
    In that case, each process will see a local device whose ID is
    the same as its local process ID.
    If None, JAX will not restrict the visible devices.
    """
    return None
