def _create_sharding_for_array(mesh, x, name, api_name):
  if x is None and (mesh is None or mesh.empty):
    return UNSPECIFIED
  if isinstance(x, XLACompatibleSharding) or is_unspecified_or_auto(x):
    return x
  if mesh is None:
    msg = ('jax.jit only supports `XLACompatibleSharding`s being passed to'
           f' {name}. Looks like you are passing either `PartitionSpec` or `None`'
           f' which is not allowed in jax.jit.\n')
    if name == 'in_shardings':
      msg += (f'Note that {name} argument is optional. JAX will infer the shardings'
              " from the input jax.Array's and will default to replicating the"
              ' input if the sharding cannot be inferred.')
    elif name == 'out_shardings':
      msg += (f'Note that {name} is optional. If not specified, jax.jit will'
              " use GSPMD's sharding propagation to figure out what the sharding"
              ' of the output(s) should be.')
    raise RuntimeError(msg)
  if mesh.empty:
    raise RuntimeError(
        f'{api_name} requires a non-empty mesh if you are passing'
        f' `PartitionSpec`s or `None` to {name}! Is a mesh defined at the call'
        f' site? Alternatively, provide `XLACompatibleSharding`s to {name} and'
        ' then the mesh context manager is not required.')
  # A nice user error is raised in prepare_axis_resources.
  assert x is None or isinstance(x, ParsedPartitionSpec), x
  return (pxla.create_mesh_pspec_sharding(mesh, x)
          if x is None else pxla.create_mesh_pspec_sharding(mesh, x.user_spec, x))
