def pure_callback_impl(
    *args,
    result_avals,
    callback: Callable[..., Any],
    sharding: SingleDeviceSharding | None,
    vectorized: bool,
):
  del sharding, vectorized, result_avals
  return callback(*args)
