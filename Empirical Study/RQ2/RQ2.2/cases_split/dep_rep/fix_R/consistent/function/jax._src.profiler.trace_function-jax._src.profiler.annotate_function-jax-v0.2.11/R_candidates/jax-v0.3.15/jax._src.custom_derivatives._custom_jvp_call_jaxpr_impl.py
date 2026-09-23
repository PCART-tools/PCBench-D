def _custom_jvp_call_jaxpr_impl(*args, fun_jaxpr: core.ClosedJaxpr, **params):
  del params  # other params ignored because we're just executing the primal fun
  return core.jaxpr_as_fun(fun_jaxpr)(*args)
