@psum_p.def_custom_bind
def psum_bind(*args, axes, axis_index_groups):
  if all(not isinstance(x, core.Tracer) for x in args):
    named_axes, pos_axes = axes_partition = [], []
    for axis in axes:
      axes_partition[isinstance(axis, int)].append(axis)
    def pos_reduce(x):
      if not pos_axes:
        return x
      return lax._reduce_sum(x, [canonicalize_axis(axis, getattr(x, 'ndim', 0))
                                 for axis in pos_axes])
    if axis_index_groups is not None:
      assert not pos_axes
      size = len(axis_index_groups[0])
    else:
      size = prod([core.axis_frame(name).size for name in named_axes])  # type: ignore
    return tuple(lax._const(x, size) * pos_reduce(x) for x in args)
  return core.AxisPrimitive.bind(
      psum_p, *args, axes=axes, axis_index_groups=axis_index_groups)
