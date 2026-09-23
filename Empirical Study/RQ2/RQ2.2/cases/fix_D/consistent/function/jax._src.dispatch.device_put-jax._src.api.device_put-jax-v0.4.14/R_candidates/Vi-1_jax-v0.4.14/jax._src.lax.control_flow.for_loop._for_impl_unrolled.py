def _for_impl_unrolled(body, nsteps, unroll, *args):
  remainder = nsteps % unroll
  i = jnp.int32(0)
  state = list(args)

  for _ in range(remainder):
    state = body(i, state)
    i = i + 1

  def cond(carry):
    i, _ = carry
    return i < nsteps
  def while_body(carry):
    i, state = carry
    for _ in range(unroll):
      state = body(i, state)
      i = i + 1
    return i, state
  _, state = lax.while_loop(cond, while_body, (i, state))
  return state
