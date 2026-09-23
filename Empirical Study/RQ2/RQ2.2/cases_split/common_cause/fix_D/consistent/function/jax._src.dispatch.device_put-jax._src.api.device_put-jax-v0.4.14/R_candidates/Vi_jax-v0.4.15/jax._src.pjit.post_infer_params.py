def post_infer_params(fun, infer_params_fn, static_argnums, static_argnames,
                      donate_argnums, abstracted_axes,
                      pjit_has_explicit_sharding):
  if abstracted_axes is None:
    wrapped = _cpp_pjit(fun, infer_params_fn, static_argnums, static_argnames,
                        donate_argnums, pjit_has_explicit_sharding)
  else:
    wrapped = _python_pjit(fun, infer_params_fn)

  @api_boundary
  def lower(*args, **kwargs):
    _experimental_lowering_platform = kwargs.pop(
        '_experimental_lowering_platform', None)
    _experimental_override_lowering_rules = kwargs.pop(
        '_experimental_override_lowering_rules', None)
    (args_flat, flat_global_in_avals, params, in_tree, out_tree,
     donated_invars) = infer_params_fn(*args, **kwargs)
    resource_env = params['resource_env']
    mesh = None if resource_env is None else resource_env.physical_mesh
    try:
      in_shardings = _resolve_in_shardings(
          args_flat, params['in_shardings'], params['out_shardings'], mesh)
      lowering = _pjit_lower(
          params['jaxpr'], in_shardings, params['out_shardings'],
          params['resource_env'], params['donated_invars'], params['name'],
          params['keep_unused'], params['inline'], always_lower=True,
          lowering_platform=_experimental_lowering_platform,
          override_lowering_rules=_experimental_override_lowering_rules)
    except pxla.DeviceAssignmentMismatchError as e:
      fails, = e.args
      api_name = 'jit' if params['resource_env'] is None else 'pjit'
      arg_names = _get_arg_names(fun, in_tree, args_flat)
      fun_name = getattr(fun, '__qualname__', getattr(fun, '__name__', str(fun)))
      msg = _device_assignment_mismatch_error(
          fun_name, fails, args_flat, api_name, arg_names)
      raise ValueError(msg) from None

    if kwargs:
      args_kwargs_in_tree = in_tree
    else:
      args_kwargs_in_tree = treedef_tuple([in_tree, tree_flatten({})[1]])

    donate_argnums = tuple(i for i, d in enumerate(donated_invars) if d)
    return stages.Lowered.from_flat_info(
        lowering, args_kwargs_in_tree, flat_global_in_avals, donate_argnums,
        out_tree)

  wrapped.lower = lower
  return wrapped
