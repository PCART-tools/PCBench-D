def _convert_elt_type_fwd_rule(eqn):
  v, = eqn.invars
  if (not core.is_opaque_dtype(eqn.params['new_dtype']) and
      not core.is_opaque_dtype(v.aval.dtype) and
      v.aval.dtype == eqn.params['new_dtype'] and
      v.aval.weak_type == eqn.params['weak_type']):
    return [v], None
  else:
    return [None], eqn
