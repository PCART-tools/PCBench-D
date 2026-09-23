def _scan_masking_rule(padded_vals, logical_shapes, reverse, length,
                       jaxpr, num_consts, num_carry, linear, unroll):
  dynamic_length, = masking.shape_as_value((length,))
  masked_jaxpr = _masked_scan_jaxpr(jaxpr, num_consts, num_carry)
  consts, init, xs = split_list(padded_vals, [num_consts, num_carry])
  max_length, = {x.shape[0] for x in xs}
  const_linear, init_linear, xs_linear = split_list(linear, [num_consts, num_carry])
  dynamic_length = lax.convert_element_type(dynamic_length, dtypes.int_)
  out_vals = scan_p.bind(dynamic_length, *consts, dtypes.int_(0), *init, *xs,
      reverse=reverse, length=max_length, jaxpr=masked_jaxpr,
      num_consts=1 + num_consts, num_carry=1 + num_carry,
      linear=tuple([False] + const_linear + [False] + init_linear + xs_linear),
      unroll=unroll)
  return out_vals[1:]
