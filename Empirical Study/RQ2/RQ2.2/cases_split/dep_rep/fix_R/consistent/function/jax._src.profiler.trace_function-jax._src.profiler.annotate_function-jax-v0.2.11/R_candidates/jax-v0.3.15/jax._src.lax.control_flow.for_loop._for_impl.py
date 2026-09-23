def _for_impl(*args, jaxpr, nsteps, reverse, which_linear):
  del which_linear
  discharged_jaxpr, consts = discharge_state(jaxpr, ())
  def cond(carry):
    i, _ = carry
    return i < nsteps
  def body(carry):
    i, state = carry
    i_ = nsteps - i - 1 if reverse else i
    next_state = core.eval_jaxpr(discharged_jaxpr, consts, i_, *state)
    return i + 1, next_state
  _, state = lax.while_loop(cond, body, (jnp.int32(0), list(args)))
  return state
