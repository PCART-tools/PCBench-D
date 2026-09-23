def _canonicalize_dimension(dim: DimSize) -> DimSize:
  # Dimensions are most commonly integral (by far), so we check that first.
  try:
    return operator.index(dim)
  except TypeError as e:
    type_error = e
  if isinstance(dim, Tracer) and config.dynamic_shapes.value:
    if not (dim.ndim == 0 and (dtypes.issubdtype(dim.dtype, np.integer)
                               or isinstance(dim.dtype, bint))):
      raise TypeError(f"Dimensions must be integer scalars; got {dim.ndim=} {dim.dtype=}")
    return dim
  elif (config.dynamic_shapes.value and isinstance(dim, DArray) and
        type(dim._aval.dtype) is bint and not dim._aval.shape):
    return dim
  elif is_dim(dim):
    return dim
  else:
    raise type_error
