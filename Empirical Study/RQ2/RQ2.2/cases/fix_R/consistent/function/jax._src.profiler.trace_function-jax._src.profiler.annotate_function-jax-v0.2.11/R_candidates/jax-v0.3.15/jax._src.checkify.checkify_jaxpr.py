def checkify_jaxpr(jaxpr, error, enabled_errors):
  f = lu.wrap_init(core.jaxpr_as_fun(jaxpr))
  return checkify_fun_to_jaxpr(f, error, enabled_errors, jaxpr.in_avals)
