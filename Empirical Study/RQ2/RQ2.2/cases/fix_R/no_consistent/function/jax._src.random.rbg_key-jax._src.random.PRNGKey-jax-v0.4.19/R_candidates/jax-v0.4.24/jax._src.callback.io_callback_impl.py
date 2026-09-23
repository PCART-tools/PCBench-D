def io_callback_impl(
    *args,
    result_avals,
    callback: Callable[..., Any],
    sharding: SingleDeviceSharding | None,
    ordered: bool,
):
  del result_avals, sharding, ordered
  return callback(*args)
