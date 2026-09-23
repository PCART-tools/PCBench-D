  @classmethod
  def from_axis_resources(cls,
                          axis_resources: dict[AxisName, tuple[ResourceAxisName, ...]],
                          resource_env: ResourceEnv,
                          global_axis_sizes: dict[AxisName, int]):
    physical_axis_resources, loop_axis_resources = _unzip_axis_resources(
            axis_resources, resource_env)
    axis_resource_count = _get_axis_resource_count(
        axis_resources, resource_env)
    axis_subst_dict = dict(axis_resources)
    axis_vmap_size: dict[AxisName, int | None] = {}
    for naxis, raxes in sorted(axis_resources.items(), key=lambda x: str(x[0])):
      num_resources = axis_resource_count[naxis]
      assert global_axis_sizes[naxis] % num_resources.nglobal == 0
      local_tile_size = global_axis_sizes[naxis] // num_resources.nglobal
      # We have to vmap when there are no resources (to handle the axis name!) or
      # when every resource gets chunks of values.
      if not raxes or local_tile_size > 1:
        axis_vmap_size[naxis] = local_tile_size
        axis_subst_dict[naxis] += (fresh_resource_name(naxis),)
      else:
        axis_vmap_size[naxis] = None
    return cls(resource_env,
               physical_axis_resources, loop_axis_resources,
               axis_subst_dict, axis_vmap_size)
