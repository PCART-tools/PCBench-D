  def output_shardings(self) -> Sequence[jax.sharding.XLACompatibleSharding]:
    raise NotImplementedError(
        "compiled executable carries no output sharding information")
