def _convert_elt_type_fwd_rule(eqn):
  v, = eqn.invars
  if (not dtypes.issubdtype(eqn.params['new_dtype'], dtypes.extended) and
      not dtypes.issubdtype(v.aval.dtype, dtypes.extended) and
      v.aval.dtype == eqn.params['new_dtype'] and
      v.aval.weak_type == eqn.params['weak_type']):
    return [v], None
  else:
    return [None], eqn
