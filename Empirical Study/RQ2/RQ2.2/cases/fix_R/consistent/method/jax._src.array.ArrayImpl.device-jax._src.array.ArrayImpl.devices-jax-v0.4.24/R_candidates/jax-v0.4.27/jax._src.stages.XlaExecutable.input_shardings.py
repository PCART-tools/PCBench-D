  def input_shardings(self) -> Sequence[jax.sharding.XLACompatibleSharding]:
    raise NotImplementedError(
        "compiled executable carries no input sharding information")
