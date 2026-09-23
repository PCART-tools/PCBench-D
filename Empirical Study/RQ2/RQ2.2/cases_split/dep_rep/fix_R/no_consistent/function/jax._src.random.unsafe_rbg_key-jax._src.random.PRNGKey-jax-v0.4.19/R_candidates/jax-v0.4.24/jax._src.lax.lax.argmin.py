def argmin(operand: ArrayLike, axis: int,
           index_dtype: DTypeLike) -> Array:
  """Computes the index of the minimum element along ``axis``."""
  return argmin_p.bind(operand, axes=(axis,),
                       index_dtype=dtypes.canonicalize_dtype(index_dtype))
