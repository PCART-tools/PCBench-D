def post_infer_params(fun, infer_params_fn, static_argnums, static_argnames,
                      donate_argnums, abstracted_axes,
                      pjit_has_explicit_sharding):
  if FLAGS.experimental_cpp_pjit and abstracted_axes is None:
    wrapped = _cpp_pjit(fun, infer_params_fn, static_argnums, static_argnames,
                        donate_argnums, pjit_has_explicit_sharding)
  else:
    wrapped = _python_pjit(fun, infer_params_fn)

  @api_boundary
  def lower(*args, _experimental_lowering_platform: Optional[str] = None,
            **kwargs):
    (args_flat, flat_local_in_avals, params, in_tree, out_tree,
     donate_argnums) = infer_params_fn(*args, **kwargs)
    if jax.config.jax_array:
      resource_env = params['resource_env']
      mesh = None if resource_env is None else resource_env.physical_mesh
      in_shardings = _resolve_in_shardings(
          args_flat, params['in_shardings'], params['out_shardings'], mesh)
    else:
      in_shardings = params['in_shardings']
    in_is_global = _calc_is_global_sequence(
        params['in_positional_semantics'], in_shardings)
    lowering = _pjit_lower(
        params['jaxpr'], in_shardings, params['out_shardings'],
        params['resource_env'], params['donated_invars'], params['name'],
        in_is_global, params['keep_unused'], always_lower=True,
        lowering_platform=_experimental_lowering_platform)

    if kwargs:
      args_kwargs_in_tree = in_tree
    else:
      args_kwargs_in_tree = treedef_tuple([in_tree, tree_flatten({})[1]])

    return stages.Lowered.from_flat_info(
        lowering, args_kwargs_in_tree, flat_local_in_avals, donate_argnums,
        out_tree)

  wrapped.lower = lower
  return wrapped
