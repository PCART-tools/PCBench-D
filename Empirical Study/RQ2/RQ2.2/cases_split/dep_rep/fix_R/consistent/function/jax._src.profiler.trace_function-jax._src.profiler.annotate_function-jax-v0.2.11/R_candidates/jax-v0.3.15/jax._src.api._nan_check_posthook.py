def _nan_check_posthook(fun, args, kwargs, output):
  """Hook function called by the C++ jit/pmap to perform NaN checking."""
  leaves = tree_leaves(output)

  buffers = []
  for da_or_sda in leaves:
    if hasattr(da_or_sda, "device_buffer"):
      buffers.append(da_or_sda.device_buffer)
    elif hasattr(da_or_sda, "device_buffers"):
      buffers.extend(da_or_sda.device_buffers)

  try:
    dispatch.check_special(xla.xla_call_p, buffers)
  except FloatingPointError:
    # compiled_fun can only raise in this case
    assert config.jax_debug_nans or config.jax_debug_infs
    print("Invalid nan value encountered in the output of a C++-jit/pmap "
          "function. Calling the de-optimized version.")
    fun._cache_miss(*args, **kwargs)[0]  # probably won't return
