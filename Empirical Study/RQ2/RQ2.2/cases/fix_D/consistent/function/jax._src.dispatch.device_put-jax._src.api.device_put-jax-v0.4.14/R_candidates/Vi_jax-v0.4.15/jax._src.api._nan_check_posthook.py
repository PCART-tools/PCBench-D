def _nan_check_posthook(fun, args, kwargs, output):
  """Hook function called by the C++ jit/pmap to perform NaN checking."""
  buffers = []
  for leaf in tree_leaves(output):
    if hasattr(leaf, "device_buffers"):
      buffers.extend(leaf.device_buffers)

  try:
    dispatch.check_special(pjit.pjit_p.name, buffers)
  except FloatingPointError:
    # compiled_fun can only raise in this case
    assert config.jax_debug_nans or config.jax_debug_infs
    print("Invalid nan value encountered in the output of a C++-jit/pmap "
          "function. Calling the de-optimized version.")
    fun._cache_miss(*args, **kwargs)[0]  # probably won't return
