def _jax_array_use_fast_path(execute, out_pytree_def, args_flat, out_flat):
  use_fastpath = (
      # This is if we have already executed this code-path (most-recent entry
      # has been reset to None). Thus, we do not support the fast-path.
      execute is not None and
      type(execute) is pxla.ExecuteReplicated and
      len(execute._local_devices) == 1 and
      # No effects in computation
      not execute.ordered_effects and
      not execute.has_unordered_effects and
      not execute.has_host_callbacks and
      all(isinstance(x, xc.ArrayImpl) for x in out_flat) and
      # Not supported: dynamic shapes
      not jax.config.jax_dynamic_shapes
      # TODO(chky): Check sharding is SingleDeviceSharding
  )

  if use_fastpath:
    sticky_device = None
    lazy_exprs = [None] * len(out_flat)
    kept_var_bitvec = [i in execute.kept_var_idx for i in range(len(args_flat))]
    avals = [out.aval for out in out_flat]
    shardings = [out.sharding for out in out_flat]
    committed = [out._committed for out in out_flat]

    return _FastpathData(execute.xla_executable, out_pytree_def, sticky_device,
                         avals, lazy_exprs, kept_var_bitvec, shardings,
                         committed)

  return None
