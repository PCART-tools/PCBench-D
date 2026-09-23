def _check_out_avals_vs_out_axes(out_avals: Sequence[core.AbstractValue],
                                 out_axes: Sequence[AxisNamePos],
                                 global_axis_sizes: Dict[AxisName, int]):
  defined_axes = set(global_axis_sizes)
  for aval, axes in zip(out_avals, out_axes):
    if not isinstance(aval, core.ShapedArray):
      if axes:
        raise AssertionError(f"Only array abstract values can have non-empty "
                             f"out_axes, but {aval} has {axes}")
      continue
    undeclared_axes = (set(aval.named_shape) - set(axes)) & defined_axes
    if undeclared_axes:
      undeclared_axes_str = sorted(str(axis) for axis in undeclared_axes)
      raise TypeError(f"One of xmap results has an out_axes specification of "
                      f"{axes.user_repr}, but is actually mapped along more axes "
                      f"defined by this xmap call: {', '.join(undeclared_axes_str)}")
