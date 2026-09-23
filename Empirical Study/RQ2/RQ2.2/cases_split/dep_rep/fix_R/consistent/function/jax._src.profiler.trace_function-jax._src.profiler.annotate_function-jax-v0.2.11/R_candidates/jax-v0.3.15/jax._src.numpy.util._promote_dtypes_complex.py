def _promote_dtypes_complex(*args):
  """Convenience function to apply Numpy argument dtype promotion.

  Promotes arguments to a complex type."""
  to_dtype, weak_type = dtypes._lattice_result_type(*args)
  to_dtype = dtypes.canonicalize_dtype(to_dtype)
  to_dtype_complex = dtypes._to_complex_dtype(to_dtype)
  return [lax_internal._convert_element_type(x, to_dtype_complex, weak_type)
          for x in args]
