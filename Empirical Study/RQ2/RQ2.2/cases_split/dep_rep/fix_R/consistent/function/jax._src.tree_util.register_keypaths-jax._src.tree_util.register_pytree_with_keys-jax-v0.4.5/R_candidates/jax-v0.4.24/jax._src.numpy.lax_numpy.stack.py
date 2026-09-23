@util.implements(np.stack, skip_params=['out'])
def stack(arrays: np.ndarray | Array | Sequence[ArrayLike],
          axis: int = 0, out: None = None, dtype: DTypeLike | None = None) -> Array:
  if not len(arrays):
    raise ValueError("Need at least one array to stack.")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.stack is not supported.")
  if isinstance(arrays, (np.ndarray, Array)):
    axis = _canonicalize_axis(axis, arrays.ndim)
    return concatenate(expand_dims(arrays, axis + 1), axis=axis, dtype=dtype)
  else:
    util.check_arraylike("stack", *arrays)
    shape0 = shape(arrays[0])
    axis = _canonicalize_axis(axis, len(shape0) + 1)
    new_arrays = []
    for a in arrays:
      if shape(a) != shape0:
        raise ValueError("All input arrays must have the same shape.")
      new_arrays.append(expand_dims(a, axis))
    return concatenate(new_arrays, axis=axis, dtype=dtype)
