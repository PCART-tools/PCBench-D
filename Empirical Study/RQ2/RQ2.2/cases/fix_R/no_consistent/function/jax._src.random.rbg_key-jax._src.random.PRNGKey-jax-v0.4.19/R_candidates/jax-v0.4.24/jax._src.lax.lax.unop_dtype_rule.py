def unop_dtype_rule(result_dtype, accepted_dtypes, name, aval, **kwargs):
  if not any(dtypes.issubdtype(aval.dtype, t) for t in accepted_dtypes):
    msg = '{} does not accept dtype {}. Accepted dtypes are subtypes of {}.'
    typename = dtype_to_string(aval.dtype)
    accepted_typenames = (t.__name__ for t in accepted_dtypes)
    raise TypeError(msg.format(name, typename, ', '.join(accepted_typenames)))
  return result_dtype(aval.dtype)
