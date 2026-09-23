def _python_pjit_helper(fun, infer_params_fn, *args, **kwargs):
  args_flat, _, params, _, out_tree, _, _, _, arg_names, attrs_tracked = \
      infer_params_fn(*args, **kwargs)
  for arg in args_flat:
    dispatch.check_arg(arg)
  if attrs_tracked:
    init_states = _get_states(attrs_tracked)
    args_flat = [*init_states, *args_flat]
  try:
    out_flat = pjit_p.bind(*args_flat, **params)
  except pxla.DeviceAssignmentMismatchError as e:
    fails, = e.args
    api_name = 'jit' if params['resource_env'] is None else 'pjit'
    fun_name = getattr(fun, '__qualname__', getattr(fun, '__name__', str(fun)))
    msg = _device_assignment_mismatch_error(
        fun_name, fails, args_flat, api_name, arg_names)
    raise ValueError(msg) from None
  if attrs_tracked:
    final_states, out_flat = split_list(out_flat, [len(attrs_tracked)])
    _set_states(attrs_tracked, final_states)
  outs = tree_unflatten(out_tree, out_flat)
  return outs, out_flat, out_tree, args_flat, params['jaxpr'], attrs_tracked
