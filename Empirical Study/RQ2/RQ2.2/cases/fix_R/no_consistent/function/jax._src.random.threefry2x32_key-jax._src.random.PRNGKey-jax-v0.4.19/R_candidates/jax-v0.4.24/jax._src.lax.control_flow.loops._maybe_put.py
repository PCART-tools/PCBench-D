def _maybe_put(x):
  if isinstance(x, np.ndarray):
    return dispatch._put_x(
        x,
        jax.sharding.SingleDeviceSharding(jax.local_devices(backend='cpu')[0]),
        shaped_abstractify(x),
        False,
    )
  else:
    return x
