def canonicalize_dim(d: DimSize, context: str="") -> DimSize:
  """Canonicalizes and checks for errors in a user-provided shape dimension value.

  Args:
    f: a Python value that represents a dimension.

  Returns:
    A canonical dimension value.
  """
  return canonicalize_shape((d,), context)[0]
