def _resource_typing_xmap(avals,
                          params,
                          source_info: source_info_util.SourceInfo,
                          resource_env,
                          outer_axis_resources):
  axis_resources = params['axis_resources']
  inner_axis_resources = dict(outer_axis_resources)
  inner_axis_resources.update(axis_resources)
  if len(inner_axis_resources) < len(outer_axis_resources) + len(axis_resources):
    overlap = set(outer_axis_resources) & set(axis_resources)
    raise JAXTypeError(
        f"Detected disallowed xmap axis name shadowing at "
        f"{source_info_util.summarize(source_info)} "
        f"(shadowed axes: {mesh_lib.show_axes(overlap)})")

  if resource_env.physical_mesh != params['resource_env'].physical_mesh:
    raise RuntimeError("Changing the physical mesh is not allowed inside xmap.")

  call_jaxpr = params['call_jaxpr']
  pxla.resource_typecheck(
      params['call_jaxpr'], resource_env, inner_axis_resources,
      lambda: (f"an xmapped function {params['name']} " +
               (f"(xmap called at {source_info_util.summarize(source_info)})"
                if source_info else "")))

  for v, axes in zip(call_jaxpr.outvars, params['out_axes']):
    broadcast_axes = set(axes) - set(v.aval.named_shape)
    used_resources = set(it.chain.from_iterable(
        inner_axis_resources[a] for a in v.aval.named_shape))
    for baxis in broadcast_axes:
      baxis_resources = set(inner_axis_resources[baxis])
      overlap = baxis_resources & used_resources
      if overlap:
        resource_to_axis = {}
        for axis in v.aval.named_shape:
          for raxis in inner_axis_resources[axis]:
            resource_to_axis[raxis] = axis
        partitioning_axes = {resource_to_axis[raxis] for raxis in overlap}
        raise JAXTypeError(
            f"One of xmapped function ({params['name']}) outputs is broadcast "
            f"along axis `{baxis}` which is assigned to resources "
            f"{mesh_lib.show_axes(baxis_resources)}, but the output is already "
            f"partitioned along {mesh_lib.show_axes(overlap)}, because its "
            f"named shape contains {mesh_lib.show_axes(partitioning_axes)}")
