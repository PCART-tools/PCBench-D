def _promote_dtypes_inexact(*args: ArrayLike) -> List[Array]:
  """Convenience function to apply Numpy argument dtype promotion.

  Promotes arguments to an inexact type."""
  to_dtype, weak_type = dtypes._lattice_result_type(*args)
  to_dtype = dtypes.canonicalize_dtype(to_dtype)
  to_dtype_inexact = dtypes.to_inexact_dtype(to_dtype)
  return [lax._convert_element_type(x, to_dtype_inexact, weak_type)
          for x in args]
