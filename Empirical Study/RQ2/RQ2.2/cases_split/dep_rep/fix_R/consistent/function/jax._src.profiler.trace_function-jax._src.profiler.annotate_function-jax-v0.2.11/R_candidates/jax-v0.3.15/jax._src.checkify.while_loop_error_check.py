def while_loop_error_check(error, enabled_errors, *in_flat, cond_nconsts,
                           cond_jaxpr, body_nconsts, body_jaxpr):
  c_consts, b_consts, carry = split_list(in_flat, [cond_nconsts, body_nconsts])

  # Check if the first cond application will error.
  checked_cond_jaxpr, msgs_cond = checkify_jaxpr(cond_jaxpr, error,
                                                 enabled_errors)
  cond_err, cond_code, cond_payload, _ = core.jaxpr_as_fun(checked_cond_jaxpr)(
      error.err, error.code, error.payload, *c_consts, *carry)

  checked_body_jaxpr_, msgs_body = checkify_while_body_jaxpr(
    cond_jaxpr, body_jaxpr, error, enabled_errors, c_consts)
  to_move = [False] * 3 + [True] * body_nconsts + [False] * len(carry)
  checked_body_jaxpr = pe.move_binders_to_front(checked_body_jaxpr_, to_move)

  compat_cond_jaxpr_ = ignore_error_output_jaxpr(checked_cond_jaxpr)
  to_move = [False] * 3 + [True] * cond_nconsts + [False] * len(carry)
  compat_cond_jaxpr = pe.move_binders_to_front(compat_cond_jaxpr_, to_move)
  new_in_flat = [*c_consts, *b_consts, cond_err, cond_code, cond_payload, *carry]

  err, code, payload, *out = lax.while_p.bind(
      *new_in_flat, cond_nconsts=cond_nconsts, cond_jaxpr=compat_cond_jaxpr,
      body_nconsts=body_nconsts, body_jaxpr=checked_body_jaxpr)
  new_msgs = {**error.msgs, **msgs_body, **msgs_cond}
  return out, Error(err, code, new_msgs, payload)
