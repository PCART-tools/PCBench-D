def scan_error_check(error, enabled_errors, *in_flat, reverse, length, jaxpr,
                     num_consts, num_carry, linear, unroll):
  consts, carry, xs = split_list(in_flat, [num_consts, num_carry])
  checked_jaxpr_, msgs_ = checkify_jaxpr(jaxpr, error, enabled_errors)
  tomove = [False] * 3 + [True] * len(consts) + [False] * (len(carry) + len(xs))
  checked_jaxpr = pe.move_binders_to_front(checked_jaxpr_, tomove)
  new_linear = (False, False, False, *linear)
  new_in_flat = [*consts, error.err, error.code, error.payload, *carry, *xs]
  err, code, payload, *outs = lax.scan_p.bind(
      *new_in_flat, reverse=reverse, length=length, jaxpr=checked_jaxpr,
      num_consts=len(consts), num_carry=len(carry)+3,
      linear=new_linear, unroll=unroll)
  new_msgs = {**error.msgs, **msgs_}
  return outs, Error(err, code, new_msgs, payload)
