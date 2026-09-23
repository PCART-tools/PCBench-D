def _get_axis_sizes(args_flat: Iterable[Any],
                    in_axes_flat: Iterable[AxisNamePos],
                    global_axis_sizes: dict[AxisName, int],
                    axis_resource_count: dict[AxisName, ResourceCount]):
  global_axis_sizes = dict(global_axis_sizes)
  for arg, in_axes in zip(args_flat, in_axes_flat):
    for name, dim in in_axes.items():
      try:
        dim_size = arg.shape[dim]
      except IndexError:
        # TODO(apaszke): Handle negative indices. Check for overlap too!
        raise ValueError(f"One of xmap arguments has an in_axes specification of "
                         f"{in_axes.user_repr}, which implies that it has at least "
                         f"{max(in_axes.values()) + 1} dimensions, but the argument "
                         f"has rank {arg.ndim}")
      global_dim_size = dim_size
      if name in global_axis_sizes:
        expected_global_dim_size = global_axis_sizes[name]
        if global_dim_size != expected_global_dim_size:
          raise ValueError(f"The size of axis {name} was previously inferred to be "
                            f"{expected_global_dim_size}, but found an argument of shape {arg.shape} "
                            f"with in_axes specification {in_axes.user_repr}. Shape mismatch "
                            f"occurs in dimension {dim}: {global_dim_size} != {expected_global_dim_size}")
      global_axis_sizes[name] = global_dim_size
  return FrozenDict(global_axis_sizes)
