def common_infer_params(pjit_info_args, *args, **kwargs):
  (fun, user_in_shardings, user_out_shardings, static_argnums, static_argnames,
   donate_argnums, device, backend, keep_unused, inline,
   resource_env) = pjit_info_args

  if kwargs and not _is_unspecified(user_in_shardings):
    raise ValueError(
        "pjit does not support kwargs when in_shardings is specified.")

  if resource_env is not None:
    pjit_mesh = resource_env.physical_mesh
    if pjit_mesh.empty:
      if jax.config.jax_array:
        # Don't enforce requiring a mesh when `jax_array` flag is enabled. But
        # if mesh is not empty then pjit will respect it.
        pass
      else:
        raise RuntimeError("pjit requires a non-empty mesh! Are you sure that "
                            "it's defined at the call site?")
  else:
    pjit_mesh = None

  if (backend or device) and pjit_mesh is not None and not pjit_mesh.empty:
    raise ValueError(
        "Mesh context manager should not be used with jit when backend or "
        "device is also specified as an argument to jit.")

  f = lu.wrap_init(fun)
  f, dyn_args = argnums_partial_except(f, static_argnums, args,
                                        allow_invalid=True)
  del args

  # TODO(yashkatariya): Merge the nokwargs and kwargs path. One blocker is
  # flatten_axes which if kwargs are present in the treedef (even empty {}),
  # leads to wrong expansion.
  if kwargs:
    f, dyn_kwargs = argnames_partial_except(f, static_argnames, kwargs)
    args_flat, in_tree = tree_flatten((dyn_args, dyn_kwargs))
    flat_fun, out_tree = flatten_fun(f, in_tree)
  else:
    args_flat, in_tree = tree_flatten(dyn_args)
    flat_fun, out_tree = flatten_fun_nokwargs(f, in_tree)
    dyn_kwargs = ()
  del kwargs

  if donate_argnums and not jax.config.jax_debug_nans:
    donated_invars = donation_vector(donate_argnums, dyn_args, dyn_kwargs)
  else:
    donated_invars = (False,) * len(args_flat)

  if jax.config.jax_array:
    # If backend or device is set as an arg on jit, then resolve them to
    # in_shardings and out_shardings as if user passed in in_shardings
    # and out_shardings.
    if backend or device:
      in_shardings = out_shardings = _create_sharding_with_device_backend(
          device, backend)
    else:
      in_shardings = tree_map(
          lambda x: _create_sharding_for_array(pjit_mesh, x), user_in_shardings)
      out_shardings = tree_map(
          lambda x: _create_sharding_for_array(pjit_mesh, x), user_out_shardings)
  else:
    in_shardings = tree_map(
        lambda x: _create_mesh_pspec_sharding_from_parsed_pspec(pjit_mesh, x),
        user_in_shardings)
    out_shardings = tree_map(
        lambda x: x if _is_unspecified(x) else
        _create_mesh_pspec_sharding_from_parsed_pspec(pjit_mesh, x), user_out_shardings)
    # This check fails extremely rarely and has a huge cost in the dispatch
    # path. So hide it behind the jax_enable_checks flag.
    if jax.config.jax_enable_checks:
      _maybe_check_pjit_gda_mesh(args_flat, pjit_mesh)

  del user_in_shardings, user_out_shardings

  local_in_avals = tuple(shaped_abstractify(a) for a in args_flat)
  # TODO(yashkatariya): This is a hack. This should go away when avals have
  # is_global attribute.
  if jax.config.jax_array:
    in_positional_semantics = (pxla._PositionalSemantics.GLOBAL,) * len(args_flat)
  else:
    in_positional_semantics = tuple(tree_map(_get_in_positional_semantics, args_flat))
  out_positional_semantics = (
      pxla._PositionalSemantics.GLOBAL
      if jax.config.jax_parallel_functions_output_gda or jax.config.jax_array else
      pxla.positional_semantics.val)

  global_in_avals, canonicalized_in_shardings_flat = _process_in_axis_resources(
      hashable_pytree(in_shardings), local_in_avals, in_tree, in_positional_semantics,
      tuple(isinstance(a, GDA) for a in args_flat), resource_env)

  jaxpr, consts, canonicalized_out_shardings_flat = _pjit_jaxpr(
      flat_fun, hashable_pytree(out_shardings), global_in_avals,
      HashableFunction(out_tree, closure=()),
      ('jit' if resource_env is None else 'pjit'))

  if (any(_is_from_gda(i) for i in canonicalized_in_shardings_flat) or
      not jax.config.jax_array):
    canonicalized_in_shardings_flat = _maybe_replace_from_gda_with_pspec(
        canonicalized_in_shardings_flat, args_flat)

  assert len(args_flat) == len(canonicalized_in_shardings_flat)

  canonicalized_in_shardings_flat = (
      _UNSPECIFIED,) * len(consts) + canonicalized_in_shardings_flat
  donated_invars = (False,) * len(consts) + donated_invars
  in_positional_semantics = (
      pxla._PositionalSemantics.GLOBAL,) * len(consts) + in_positional_semantics

  # in_shardings and out_shardings here are all GSPMDSharding.
  params = dict(
      jaxpr=jaxpr,
      in_shardings=canonicalized_in_shardings_flat,
      out_shardings=canonicalized_out_shardings_flat,
      resource_env=resource_env,
      donated_invars=donated_invars,
      name=getattr(flat_fun, '__name__', '<unnamed function>'),
      in_positional_semantics=in_positional_semantics,
      out_positional_semantics=out_positional_semantics,
      keep_unused=keep_unused,
      inline=inline,
  )
  return (consts + args_flat, local_in_avals, params, in_tree, out_tree(),
          donate_argnums)
