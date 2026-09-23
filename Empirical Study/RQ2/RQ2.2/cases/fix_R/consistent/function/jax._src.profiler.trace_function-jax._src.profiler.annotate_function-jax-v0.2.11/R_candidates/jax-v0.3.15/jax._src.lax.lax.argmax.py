def argmax(operand: Array, axis: int,
           index_dtype: DType) -> Tuple[Array, Array]:
  """Computes the index of the maximum element along ``axis``."""
  return argmax_p.bind(operand, axes=(axis,),
                       index_dtype=dtypes.canonicalize_dtype(index_dtype))
