  def is_equivalent_to(self, other: Sharding, ndim: int) -> bool:
    """Returns ``True`` if two shardings are equivalent.

    Two shardings are equivalent if they place the same logical array shards on
    the same devices.

    For example, a :class:`NamedSharding` may be equivalent
    to a :class:`PositionalSharding` if both place the same shards of the array
    on the same devices.
    """
    raise NotImplementedError('Subclasses should implement this method.')
