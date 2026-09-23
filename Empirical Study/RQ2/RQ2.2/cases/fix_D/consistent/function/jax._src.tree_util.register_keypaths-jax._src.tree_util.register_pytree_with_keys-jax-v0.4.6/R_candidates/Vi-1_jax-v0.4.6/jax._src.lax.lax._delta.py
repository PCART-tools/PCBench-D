def _delta(dtype: DTypeLike, shape: Shape, axes: Sequence[int]) -> Array:
  """This utility function exists for creating Kronecker delta arrays."""
  axes = map(int, axes)
  dtype = dtypes.canonicalize_dtype(dtype)
  base_shape = tuple(np.take(shape, axes))  # type: ignore[arg-type]
  iotas = [broadcasted_iota(np.uint32, base_shape, i)
           for i in range(len(base_shape))]
  eyes = [eq(i1, i2) for i1, i2 in zip(iotas[:-1], iotas[1:])]
  result = convert_element_type_p.bind(_reduce(operator.and_, eyes),
                                       new_dtype=dtype, weak_type=False)
  return broadcast_in_dim(result, shape, axes)
