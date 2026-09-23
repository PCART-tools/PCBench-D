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
    lowering_parameters = kwargs.pop(
        '_experimental_lowering_parameters', mlir.LoweringParameters())
    # TODO(yashkatariya): Remove this when it's added on jit.
    in_layouts = kwargs.pop('_in_layouts', None)
    out_layouts = kwargs.pop('_out_layouts', None)
    (args_flat, flat_global_in_avals, params, in_tree, out_tree,
     donated_invars, in_layouts_flat, out_layouts_flat,
     arg_names, ()) = infer_params_fn(
         *args, **kwargs, _in_layouts=in_layouts, _out_layouts=out_layouts)
    resource_env = params['resource_env']
    mesh = None if resource_env is None else resource_env.physical_mesh
    try:
      in_shardings = _resolve_in_shardings(
          args_flat, params['in_shardings'], params['out_shardings'], mesh)
      lowering = _pjit_lower(
          params['jaxpr'], in_shardings, params['out_shardings'],
          params['resource_env'], params['donated_invars'], params['name'],
          params['keep_unused'], params['inline'], in_layouts=in_layouts_flat,
          out_layouts=out_layouts_flat, lowering_parameters=lowering_parameters)
    except pxla.DeviceAssignmentMismatchError as e:
      fails, = e.args
      api_name = 'jit' if params['resource_env'] is None else 'pjit'
      fun_name = getattr(fun, '__qualname__', getattr(fun, '__name__', str(fun)))
      msg = _device_assignment_mismatch_error(
          fun_name, fails, args_flat, api_name, arg_names)
      raise ValueError(msg) from None

    donate_argnums = tuple(i for i, d in enumerate(donated_invars) if d)
    return stages.Lowered.from_flat_info(
        lowering, in_tree, flat_global_in_avals, donate_argnums,
        out_tree)

  @api_boundary
  def eval_shape(*args, **kwargs):
    _, _, params, _, out_tree, _, _, _, _, _ = infer_params_fn(
        *args, **kwargs, _in_layouts=None, _out_layouts=None)
    out_s = [None if is_unspecified(s) else getattr(s, '_original_sharding', s)
             for s in params['out_shardings']]
    out = [api.ShapeDtypeStruct(x.shape, x.dtype, x.named_shape, sharding=s)
           for x, s in zip(params['jaxpr'].out_avals, out_s)]
    return tree_unflatten(out_tree, out)

  wrapped.lower = lower
  wrapped.eval_shape = eval_shape
  return wrapped
