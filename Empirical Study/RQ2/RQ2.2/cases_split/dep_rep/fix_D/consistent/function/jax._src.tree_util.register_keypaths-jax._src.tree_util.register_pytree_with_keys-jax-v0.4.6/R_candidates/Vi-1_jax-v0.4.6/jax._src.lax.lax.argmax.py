def argmax(operand: ArrayLike, axis: int,
           index_dtype: DTypeLike) -> Array:
  """Computes the index of the maximum element along ``axis``."""
  return argmax_p.bind(operand, axes=(axis,),
                       index_dtype=dtypes.canonicalize_dtype(index_dtype))
