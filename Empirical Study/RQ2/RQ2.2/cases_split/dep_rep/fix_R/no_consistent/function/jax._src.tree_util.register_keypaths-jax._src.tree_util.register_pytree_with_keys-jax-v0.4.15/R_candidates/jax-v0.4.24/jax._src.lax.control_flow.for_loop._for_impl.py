def _for_impl(*args, jaxpr, nsteps, reverse, which_linear, unroll):
  del which_linear
  discharged_jaxpr, consts = discharge_state(jaxpr, ())
  def body(i, state):
    i_ = nsteps - i - 1 if reverse else i
    return core.eval_jaxpr(discharged_jaxpr, consts, i_, *state)
  return _for_impl_unrolled(body, nsteps, unroll, *args)
