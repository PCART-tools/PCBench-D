def _check_unique_resources(axis_resources, arg_name):
  for arg_axis_resources in axis_resources:
    if not arg_axis_resources: continue
    if (is_unspecified_or_auto(arg_axis_resources) or
        isinstance(arg_axis_resources, XLACompatibleSharding)):
      continue
    constrained_dims = [d for d in arg_axis_resources if d is not None]
    resource_counts = collections.Counter(
        itertools.chain.from_iterable(constrained_dims))
    if not resource_counts: continue
    if resource_counts.most_common(1)[0][1] > 1:
      multiple_uses = [r for r, c in resource_counts.items() if c > 1]
      if multiple_uses:
        raise ValueError(f"A single {arg_name} specification can map every mesh axis "
                         f"to at most one positional dimension, but {arg_axis_resources.user_spec} "
                         f"has duplicate entries for {mesh_lib.show_axes(multiple_uses)}")
