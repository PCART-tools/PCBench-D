def _get_axis_resource_count(
    axis_resources, resource_env) -> Dict[ResourceAxisName, ResourceCount]:
  global_res_shape = resource_env.shape
  local_res_shape = None

  distributed = (False if resource_env.physical_mesh.empty else
                 resource_env.physical_mesh.size != len(resource_env.physical_mesh.local_devices))
  resource_count_map = {}
  for axis, resources in axis_resources.items():
    if local_res_shape is None:
      nlocal = None
    else:
      nlocal = int(np.prod(map(local_res_shape.get, resources), dtype=np.int64))
    resource_count_map[axis] = ResourceCount(
        int(np.prod(map(global_res_shape.get, resources), dtype=np.int64)),
        nlocal, distributed)
  return resource_count_map
