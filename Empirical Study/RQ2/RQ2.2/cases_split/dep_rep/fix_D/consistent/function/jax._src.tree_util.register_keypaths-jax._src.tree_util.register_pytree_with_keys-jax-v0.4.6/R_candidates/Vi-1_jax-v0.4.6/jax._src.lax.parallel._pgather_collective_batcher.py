def _pgather_collective_batcher(axis_size, frame_name, _, vals_in, dims_in, *, axes):
  src, idx = vals_in
  dsrc, didx = dims_in
  if dsrc is batching.not_mapped:
    raise ValueError("pgather axis {frame.name} is missing from the indexed value")
  if didx is not batching.not_mapped:
    # NOTE: This is allowed and the output would be mapped along this axis!
    raise NotImplementedError("Please open a feature request!")
  # Now source is mapped, idx is not
  new_axes = tuple(dsrc if axis == frame_name else
                   axis + (dsrc <= axis) if isinstance(axis, int) else
                   axis
                   for axis in axes)
  # The result is not mapped, because we eliminate all axes, and those include
  # the batched axis.
  if all(isinstance(axis, int) for axis in axes):
    # We rewrite a purely positional pgather as a gather, because that one
    # is more fully featured (e.g. supports AD).
    return _pgather_impl(src, idx, axes=new_axes), batching.not_mapped
  else:
    return pgather_p.bind(src, idx, axes=new_axes), batching.not_mapped
