def apply_primitive(prim, *args, **params):
  """Impl rule that compiles and runs a single primitive 'prim' using XLA."""
  fun = xla_primitive_callable(prim, **params)
  # TODO(yashkatariya): Investigate adding is_primitive to jit and never
  # triggering the disable jit path instead of messing around with it here.
  if xla_extension_version >= 218:
    prev = lib.jax_jit.swap_thread_local_state_disable_jit(False)
    try:
      outs = fun(*args)
    finally:
      lib.jax_jit.swap_thread_local_state_disable_jit(prev)
  else:
    with config.disable_jit(False):
      outs = fun(*args)
  return outs
