  def input_shardings(self) -> Sequence[jax.sharding.XLACompatibleSharding]:
    """Flat sequence of input shardings.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend,
    compiler, or runtime.
    """
    raise NotImplementedError
