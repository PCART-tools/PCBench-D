def _run_state_impl(*args: Any, jaxpr: core.Jaxpr,
                    which_linear: tuple[bool, ...]):
  del which_linear
  discharged_jaxpr, consts = discharge_state(jaxpr, ())
  return core.eval_jaxpr(discharged_jaxpr, consts, *args)
