def _cast_to_bool(operand: ArrayLike) -> Array:
  with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=NumpyComplexWarning)
    return lax.convert_element_type(operand, np.bool_)
