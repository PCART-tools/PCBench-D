def _closed_call_param_updater(params, _, __):
  jaxpr = params.get('call_jaxpr')
  if jaxpr is None: return params
  assert type(jaxpr) is core.Jaxpr
  return dict(params, call_jaxpr=core.ClosedJaxpr(jaxpr, ()))
