  def output_shardings(self) -> Sequence[jax.sharding.XLACompatibleSharding]:
    """Flat sequence of output shardings.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend,
    compiler, or runtime.
    """
    raise NotImplementedError
