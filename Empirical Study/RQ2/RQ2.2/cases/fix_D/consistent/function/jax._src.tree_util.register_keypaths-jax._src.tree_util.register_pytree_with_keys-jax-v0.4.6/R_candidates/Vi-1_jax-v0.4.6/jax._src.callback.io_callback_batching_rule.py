def io_callback_batching_rule(args, dims, callback, result_avals, ordered):
  if ordered:
    raise ValueError("Cannot `vmap` ordered IO callback.")
  return pure_callback_batching_rule(args, dims, callback=callback,
      vectorized=False, result_avals=result_avals)
