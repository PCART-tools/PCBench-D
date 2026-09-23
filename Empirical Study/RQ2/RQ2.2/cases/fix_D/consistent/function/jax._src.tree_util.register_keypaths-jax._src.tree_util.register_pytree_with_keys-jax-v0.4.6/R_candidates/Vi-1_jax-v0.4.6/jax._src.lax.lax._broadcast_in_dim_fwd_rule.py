def _broadcast_in_dim_fwd_rule(eqn):
  v, *dyn = eqn.invars
  if not dyn and core.symbolic_equal_shape(eqn.params['shape'], v.aval.shape):
    return [v], None
  else:
    return [None], eqn
