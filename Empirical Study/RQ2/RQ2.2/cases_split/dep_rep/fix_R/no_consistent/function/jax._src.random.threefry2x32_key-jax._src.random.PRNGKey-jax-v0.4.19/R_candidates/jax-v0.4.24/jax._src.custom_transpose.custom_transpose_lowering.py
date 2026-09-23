def custom_transpose_lowering(*args, call_jaxpr, **params):
  return core.jaxpr_as_fun(call_jaxpr)(*args)
