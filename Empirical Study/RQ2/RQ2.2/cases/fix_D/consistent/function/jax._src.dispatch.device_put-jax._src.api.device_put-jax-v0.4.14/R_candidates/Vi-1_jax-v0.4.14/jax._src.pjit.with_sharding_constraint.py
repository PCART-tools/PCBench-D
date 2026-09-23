def with_sharding_constraint(x, shardings):
  """Mechanism to constrain the sharding of an Array inside a jitted computation

  This is a strict constraint for the GSPMD partitioner and not a hint. For examples
  of how to use this function, see `Distributed arrays and automatic parallelization`_.

  Args:
    x: PyTree of jax.Arrays which will have their shardings constrainted
    shardings: PyTree of sharding specifications. Valid values are the same as for
      the ``in_shardings`` argument of :func:`jax.experimental.pjit`.
  Returns:
    x_with_shardings: PyTree of jax.Arrays with specified sharding constraints.

  .. _Distributed arrays and automatic parallelization: https://jax.readthedocs.io/en/latest/notebooks/Distributed_arrays_and_automatic_parallelization.html
  """
  x_flat, tree = tree_flatten(x)
  user_shardings, _, _ = prepare_axis_resources(
      shardings, "shardings", allow_unconstrained_dims=True)
  del shardings

  user_shardings_flat = tuple(
      flatten_axes("with_sharding_constraint shardings", tree, user_shardings))
  del user_shardings

  resource_env = mesh_lib.thread_resources.env
  mesh = resource_env.physical_mesh

  shardings_flat = [_create_sharding_for_array(mesh, a, 'shardings',
                                               'with_sharding_constraint')
                    for a in user_shardings_flat]
  unconstrained_dims = [get_unconstrained_dims(s)
                        if isinstance(s, NamedSharding) else {}
                        for s in shardings_flat]
  del user_shardings_flat

  pjit_check_aval_sharding(
      shardings_flat, x_flat, None, "with_sharding_constraint arguments",
      allow_uneven_sharding=True)

  outs = [sharding_constraint_p.bind(xf, sharding=to_gspmd_sharding(i, xf.ndim),
                                     resource_env=resource_env,
                                     unconstrained_dims=ud)
          for xf, i, ud in zip(x_flat, shardings_flat, unconstrained_dims)]
  return tree_unflatten(tree, outs)
