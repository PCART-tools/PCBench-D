def _device_array_use_fast_path(execute, out_pytree_def, args_flat, out_flat):
  # TODO(sharadmv): Clean up usage of `execute.args`
  use_fastpath = (
      # This is if we have already executed this code-path (most-recent entry
      # has been reset to None). Thus, we do not support the fast-path.
      execute is not None and
      execute.func is dispatch._execute_compiled and  # not trivial, not pmap
      # No effects in computation
      not execute.args[5] and not execute.args[6] and
      # Has no host callbacks
      not execute.args[8] and
      # impl rule must have been called, i.e. top trace is an EvalTrace
      isinstance(core.find_top_trace(args_flat), core.EvalTrace) and
      # Not supported: ShardedDeviceArray
      all(device_array.type_is_device_array(x) for x in out_flat) and
      # Not supported: dynamic shapes
      not jax.config.jax_dynamic_shapes
      and type(execute.args[4]) is dispatch.SimpleResultHandler)

  ### If we can use the fastpath, we return required info to the caller.
  if use_fastpath:
    (_, xla_executable, _, _, result_handlers, _, _, kept_var_idx,
     _) = execute.args  # pytype: disable=attribute-error
    sticky_device = None
    avals = []
    lazy_exprs = [None] * len(result_handlers)
    for result_handler in result_handlers:
      aval, sticky_device = result_handler.args
      avals.append(aval)
    assert len(avals) == len(out_flat)
    kept_var_bitvec = [i in kept_var_idx for i in range(len(args_flat))]
    shardings = []
    committed = []

    return _FastpathData(xla_executable, out_pytree_def, sticky_device, avals,
                         lazy_exprs, kept_var_bitvec, shardings, committed)

  return None
