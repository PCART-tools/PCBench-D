def argmin(operand: Array, axis: int,
           index_dtype: DType) -> Tuple[Array, Array]:
  """Computes the index of the minimum element along ``axis``."""
  return argmin_p.bind(operand, axes=(axis,),
                       index_dtype=dtypes.canonicalize_dtype(index_dtype))
