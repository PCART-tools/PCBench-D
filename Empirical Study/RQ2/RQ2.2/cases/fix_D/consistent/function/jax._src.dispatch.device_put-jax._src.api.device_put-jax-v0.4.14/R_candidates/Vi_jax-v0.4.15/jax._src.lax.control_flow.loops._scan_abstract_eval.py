def _scan_abstract_eval(*args, reverse, length, num_consts, num_carry, jaxpr,
                        linear, unroll):
  carry_avals, y_avals = split_list(jaxpr.out_avals, [num_carry])
  ys_avals = _map(partial(_prepend_dim_to_aval, length), y_avals)
  return carry_avals + ys_avals, jaxpr.effects
