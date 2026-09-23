def _complex_elem_type(dtype: DTypeLike) -> DType:
  """Returns the float type of the real/imaginary parts of a complex dtype."""
  return np.abs(np.zeros((), dtype)).dtype
