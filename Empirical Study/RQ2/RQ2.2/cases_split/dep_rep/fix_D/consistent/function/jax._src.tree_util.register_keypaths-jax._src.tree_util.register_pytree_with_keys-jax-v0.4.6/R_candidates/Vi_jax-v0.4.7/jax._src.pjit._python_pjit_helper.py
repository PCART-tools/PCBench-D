def _python_pjit_helper(fun, infer_params_fn, *args, **kwargs):
  args_flat, _, params, in_tree, out_tree, _ = infer_params_fn(
      *args, **kwargs)
  for arg in args_flat:
    dispatch.check_arg(arg)
  try:
    out_flat = pjit_p.bind(*args_flat, **params)
  except pxla.DeviceAssignmentMismatchError as e:
    fails, = e.args
    api_name = 'jit' if params['resource_env'] is None else 'pjit'
    arg_names = _get_arg_names(fun, in_tree, args_flat)
    fun_name = getattr(fun, '__qualname__', getattr(fun, '__name__', str(fun)))
    msg = _device_assignment_mismatch_error(
        fun_name, fails, args_flat, api_name, arg_names)
    raise ValueError(msg) from None
  outs = tree_unflatten(out_tree, out_flat)
  return outs, out_flat, out_tree, args_flat
