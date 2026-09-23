def with_sharding_constraint(x, axis_resources=_UNSPECIFIED,
                             shardings=_UNSPECIFIED):
  final_shardings = _resolve_wsc_args(axis_resources, shardings)
  x_flat, tree = tree_flatten(x)
  user_shardings, _, _ = _prepare_axis_resources(
      final_shardings, "shardings", allow_unconstrained_dims=True)
  del final_shardings

  user_shardings_flat = tuple(
      flatten_axes("with_sharding_constraint shardings", tree, user_shardings))
  del user_shardings

  resource_env = pxla.thread_resources.env
  mesh = resource_env.physical_mesh

  if config.jax_array:
    shardings_flat = [_create_sharding_for_array(mesh, a)
                      for a in user_shardings_flat]
    unconstrained_dims = [get_unconstrained_dims(s)
                          if isinstance(s, NamedSharding) else {}
                          for s in shardings_flat]
  else:
    shardings_flat = [pxla.create_mesh_pspec_sharding(mesh, a.user_spec, a)
                      for a in user_shardings_flat]
    # Calculate unconstrained_dims from NamedSharding because that information
    # is lost when converted to OpSharding. Bind unconstrained_dims to
    # with_sharding_constraint primitive.
    unconstrained_dims = [get_unconstrained_dims(s) for s in shardings_flat]

  del user_shardings_flat

  pjit_check_aval_sharding(shardings_flat, x_flat, "with_sharding_constraint arguments",
                           allow_uneven_sharding=True)

  outs = [sharding_constraint_p.bind(xf, sharding=to_gspmd_sharding(i, xf.ndim),
                                     resource_env=resource_env,
                                     unconstrained_dims=ud)
          for xf, i, ud in safe_zip(x_flat, shardings_flat, unconstrained_dims)]
  return tree_unflatten(tree, outs)
