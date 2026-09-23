def _check_gda_or_array_xmap_partitioning(axis_resources, resource_env,
                                          global_axis_sizes, in_axes_flat,
                                          args_flat):
  @lru_cache
  def _check_sharding(in_sharding, xmap_sharding, ndim, arr_flavor):
    if (not op_shardings.are_op_shardings_equal(
          in_sharding._to_xla_hlo_sharding(ndim),
          xmap_sharding._to_xla_hlo_sharding(ndim)) or
        in_sharding.memory_kind != xmap_sharding.memory_kind):
      raise ValueError(
          f"Got an input {arr_flavor} to xmap with different partitioning than "
          "specified in xmap. The partitioning must match. "
          f"Got {arr_flavor} spec: {in_sharding.spec} and "
          f"xmap spec: {xmap_sharding.spec}")

  mesh_in_axes = EvaluationPlan.from_axis_resources(  # pytype: disable=wrong-arg-types  # always-use-return-annotations
      axis_resources, resource_env, global_axis_sizes).to_mesh_axes(in_axes_flat)
  for arg, xmap_array_mapping in safe_zip(args_flat, mesh_in_axes):
    if isinstance(arg, ArrayImpl):
      if not isinstance(arg.sharding, NamedSharding):
        continue
      mesh = arg.sharding.mesh
      if mesh != resource_env.physical_mesh:
        raise ValueError("xmap's mesh and Array's mesh should be equal. "
                         f"Got xmap mesh: {resource_env.physical_mesh},\n"
                         f"Array mesh: {mesh}")

      s = arg.sharding
      xmap_sharding = pxla.create_mesh_pspec_sharding(
          mesh, array_mapping_to_axis_resources(xmap_array_mapping))
      # This check is cached because comparing OpSharding is expensive during
      # dispatch and if the shardings are the same, then there is no need to
      # compare twice.
      _check_sharding(s, xmap_sharding, arg.ndim, 'Array')
