  @property
  def device_set(self) -> set[Device]:
    """The set of devices that this :class:`Sharding` spans.

    In multi-controller JAX, the set of devices is global, i.e., includes
    non-addressable devices from other processes.
    """
    raise NotImplementedError('Subclasses should implement this method.')
