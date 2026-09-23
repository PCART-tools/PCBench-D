def _unzip_axis_resources(axis_resources: Dict[AxisName, Tuple[ResourceAxisName, ...]],
                          resource_env: ResourceEnv):
  """Splits axis_resources into separate dicts for physical and loop resources."""
  physical_axis_resources = {}
  loop_axis_resources = {}
  loop_resource_axes = resource_env.loop_resource_axes
  for axis, raxes in axis_resources.items():
    first_loop = 0
    for raxis in raxes:
      if raxis in loop_resource_axes:
        break
      else:
        first_loop += 1
    physical_axis_resources[axis] = raxes[:first_loop]
    loop_resources = loop_axis_resources[axis] = raxes[first_loop:]
    if not all(name in loop_resource_axes for name in loop_resources):
      raise NotImplementedError("Loop resources cannot appear before mesh axes "
                                "in the resource_axis argument")
  return physical_axis_resources, loop_axis_resources
