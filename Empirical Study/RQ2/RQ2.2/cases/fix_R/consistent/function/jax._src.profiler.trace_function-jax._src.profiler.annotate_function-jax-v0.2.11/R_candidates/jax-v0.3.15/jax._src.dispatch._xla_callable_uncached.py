def _xla_callable_uncached(fun: lu.WrappedFun, device, backend, name,
                           donated_invars, keep_unused, *arg_specs):
  return lower_xla_callable(fun, device, backend, name, donated_invars, False,
                            keep_unused, *arg_specs).compile().unsafe_call
