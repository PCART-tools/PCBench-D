def _xla_call_partial_eval_update_params(
    params: core.ParamDict, kept_inputs: Sequence[bool], num_new_inputs: int
  ) -> core.ParamDict:
  donated_invars = params['donated_invars']
  if not kept_inputs and donated_invars:
    # JaxprTrace.post_process_call creates a call with no input tracers
    donated_invars = (False,) * num_new_inputs
  else:
    assert len(kept_inputs) == len(donated_invars)
    # JaxprTrace.process_call drops known input tracers
    donated_invars = [d for d, kept in zip(donated_invars, kept_inputs) if kept]
    # Any new inputs are prepended to the left, so mark those as not donated.
    donated_invars = [False] * num_new_inputs + donated_invars
  return dict(params, donated_invars=tuple(donated_invars))
