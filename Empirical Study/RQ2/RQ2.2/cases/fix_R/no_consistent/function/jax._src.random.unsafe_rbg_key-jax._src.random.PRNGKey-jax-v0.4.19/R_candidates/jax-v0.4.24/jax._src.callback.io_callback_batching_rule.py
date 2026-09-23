def io_callback_batching_rule(
    args, dims, callback, result_avals, sharding, ordered
):
  if ordered:
    raise ValueError("Cannot `vmap` ordered IO callback.")
  return pure_callback_batching_rule(
      args,
      dims,
      callback=callback,
      sharding=sharding,
      vectorized=False,
      result_avals=result_avals,
  )
