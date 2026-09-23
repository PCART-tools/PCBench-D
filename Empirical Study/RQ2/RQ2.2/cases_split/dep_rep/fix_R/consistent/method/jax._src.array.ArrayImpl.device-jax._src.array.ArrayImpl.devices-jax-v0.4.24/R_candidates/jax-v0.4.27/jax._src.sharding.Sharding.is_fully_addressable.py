  @property
  def is_fully_addressable(self) -> bool:
    """Is this sharding fully addressable?

    A sharding is fully addressable if the current process can address all of
    the devices named in the :class:`Sharding`. ``is_fully_addressable`` is
    equivalent to "is_local" in multi-process JAX.
    """
    raise NotImplementedError('Subclasses should implement this method.')
