def _reduce_number_dtype_rule(name, operand, *args, **kw):
  if not dtypes.issubdtype(operand.dtype, np.number):
    raise TypeError("{} does not accept dtype {}. Accepted dtypes are subtypes "
                    "of number.".format(name, dtype_to_string(operand.dtype)))
  return dtypes.canonicalize_dtype(operand.dtype)
