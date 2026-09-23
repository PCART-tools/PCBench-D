def _linear_call_abstract_eval(*args, **kwargs):
  return map(core.raise_to_shaped, kwargs['callee'].out_avals)
