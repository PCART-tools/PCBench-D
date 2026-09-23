def _shard_abstract_array(size, axis: int, x):
  try:
    if x.shape[axis] != size:
      raise ValueError(f"Axis size {size} does not match dimension {axis} of "
                       f"shape {x.shape}")
  except IndexError:
    raise ValueError("Cannot split a {x.dim}D value along axis {axis}") from None
  if config.pmap_no_rank_reduction.value:
    return x.update(shape=tuple_update(x.shape, axis, 1))
  else:
    return x.update(shape=tuple_delete(x.shape, axis))
