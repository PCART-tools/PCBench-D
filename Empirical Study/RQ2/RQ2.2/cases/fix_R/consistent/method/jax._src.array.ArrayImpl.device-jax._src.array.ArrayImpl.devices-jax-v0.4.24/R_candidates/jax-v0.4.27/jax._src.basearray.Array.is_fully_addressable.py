  @property
  @abc.abstractmethod
  def is_fully_addressable(self) -> bool:
    """Is this Array fully addressable?

    A jax.Array is fully addressable if the current process can address all of
    the devices named in the :class:`Sharding`. ``is_fully_addressable`` is
    equivalent to "is_local" in multi-process JAX.

    Note that fully replicated is not equal to fully addressable i.e.
    a jax.Array which is fully replicated can span across multiple hosts and is
    not fully addressable.
    """
