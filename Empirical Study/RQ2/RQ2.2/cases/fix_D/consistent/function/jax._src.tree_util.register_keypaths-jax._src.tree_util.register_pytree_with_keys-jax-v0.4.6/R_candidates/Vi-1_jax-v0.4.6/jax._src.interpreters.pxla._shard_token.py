def _shard_token(x, devices, indices, sharding):
  if jax.config.jax_array:
    zeros = np.zeros((), dtype=np.dtype(np.bool_))
    aval = api_util.shaped_abstractify(zeros)
    return batched_device_put(aval, sharding, [zeros for i in indices], devices)
  return device_put(np.zeros((), dtype=np.dtype(np.bool_)), devices, replicate=True)
