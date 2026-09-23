def _sharding_constraint_batcher(insert_axis, spmd_axis_name, axis_size,
                                 axis_name, main_type, vals_in, dims_in,
                                 sharding, resource_env, unconstrained_dims):
  x, = vals_in
  d, = dims_in
  # None means unconstrained in ParsedPartitionSpec
  new_parts = (axis_name,) if insert_axis else (
      None if spmd_axis_name is None else spmd_axis_name)
  unconstrained_dims = {ud + (d <= ud) for ud in unconstrained_dims}
  if new_parts is None:
    unconstrained_dims.add(d)
  y = sharding_constraint_p.bind(
      x,
      sharding=_pjit_batcher_for_sharding(
          sharding, d, new_parts, resource_env.physical_mesh, x.ndim),
      resource_env=resource_env,
      unconstrained_dims=unconstrained_dims)
  return y, d
