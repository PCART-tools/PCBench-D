@pure_callback_p.def_abstract_eval
def pure_callback_abstract_eval(
    *avals,
    callback: Callable[..., Any],
    result_avals,
    sharding: SingleDeviceSharding | None,
    vectorized: bool,
):
  del avals, callback, sharding, vectorized
  return result_avals
