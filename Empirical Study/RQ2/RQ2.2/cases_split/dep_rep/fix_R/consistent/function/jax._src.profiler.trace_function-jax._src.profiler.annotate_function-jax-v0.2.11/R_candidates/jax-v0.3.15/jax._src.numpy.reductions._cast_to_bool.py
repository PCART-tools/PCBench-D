def _cast_to_bool(operand):
  with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=np.ComplexWarning)
    return lax.convert_element_type(operand, np.bool_)
