def common_infer_params(pjit_info_args, *args, **kwargs):
  (fun, user_in_shardings, user_out_shardings, static_argnums, static_argnames,
   donate_argnums, device, backend, keep_unused, inline,
   resource_env, abstracted_axes) = pjit_info_args

  if kwargs and not _is_unspecified(user_in_shardings):
    raise ValueError(
        "pjit does not support kwargs when in_shardings is specified.")

  if resource_env is not None:
    pjit_mesh = resource_env.physical_mesh
  else:
    pjit_mesh = None

  if (backend or device) and pjit_mesh is not None and not pjit_mesh.empty:
    raise ValueError(
        "Mesh context manager should not be used with jit when backend or "
        "device is also specified as an argument to jit.")

  axes_specs = _flat_axes_specs(abstracted_axes, *args, **kwargs)

  jit_name = 'jit' if resource_env is None else 'pjit'
  dbg = debug_info(jit_name, fun, args, kwargs, static_argnums, static_argnames)
  f = lu.wrap_init(fun)
  f, res_paths = result_paths(f)
  f, dyn_args = argnums_partial_except(f, static_argnums, args,
                                       allow_invalid=True)
  del args

  # TODO(yashkatariya): Merge the nokwargs and kwargs path. One blocker is
  # flatten_axes which if kwargs are present in the treedef (even empty {}),
  # leads to wrong expansion.
  if kwargs:
    f, dyn_kwargs = argnames_partial_except(f, static_argnames, kwargs)
    explicit_args, in_tree = tree_flatten((dyn_args, dyn_kwargs))
    flat_fun, out_tree = flatten_fun(f, in_tree)
  else:
    explicit_args, in_tree = tree_flatten(dyn_args)
    flat_fun, out_tree = flatten_fun_nokwargs(f, in_tree)
    dyn_kwargs = ()
  del kwargs

  if donate_argnums and not jax.config.jax_debug_nans:
    donated_invars = donation_vector(donate_argnums, dyn_args, dyn_kwargs)
  else:
    donated_invars = (False,) * len(explicit_args)

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

  del user_in_shardings, user_out_shardings

  if config.jax_dynamic_shapes:
    in_type = pe.infer_lambda_input_type(axes_specs, explicit_args)
    in_avals = tuple([a for a, e in in_type if e])
  else:
    in_type = in_avals = tuple(shaped_abstractify(a) for a in explicit_args)

  canonicalized_in_shardings_flat = _process_in_axis_resources(
      hashable_pytree(in_shardings), in_avals, in_tree, resource_env)

  jaxpr, consts, canonicalized_out_shardings_flat = _pjit_jaxpr(
      flat_fun, hashable_pytree(out_shardings), in_type, dbg,
      HashableFunction(out_tree, closure=()),
      HashableFunction(res_paths, closure=()))

  if any(_is_from_gda(i) for i in canonicalized_in_shardings_flat):
    canonicalized_in_shardings_flat = _maybe_replace_from_gda_with_pspec(
        canonicalized_in_shardings_flat, explicit_args)
  assert len(explicit_args) == len(canonicalized_in_shardings_flat)

  if config.jax_dynamic_shapes:
    implicit_args = _extract_implicit_args(in_type, explicit_args)
  else:
    implicit_args = []
  args_flat = [*implicit_args, *explicit_args]

  num_extra_args = len(implicit_args) + len(consts)
  canonicalized_in_shardings_flat = \
      (_UNSPECIFIED,) * num_extra_args + canonicalized_in_shardings_flat
  donated_invars = (False,) * num_extra_args + donated_invars
  assert (len(canonicalized_in_shardings_flat) == len(donated_invars) ==
          len(consts) + len(args_flat))

  # in_shardings and out_shardings here are all GSPMDSharding.
  params = dict(
      jaxpr=jaxpr,
      in_shardings=canonicalized_in_shardings_flat,
      out_shardings=canonicalized_out_shardings_flat,
      resource_env=resource_env,
      donated_invars=donated_invars,
      name=getattr(flat_fun, '__name__', '<unnamed function>'),
      keep_unused=keep_unused,
      inline=inline,
  )
  return (consts + args_flat, in_type, params, in_tree, out_tree(),
          donate_argnums)
