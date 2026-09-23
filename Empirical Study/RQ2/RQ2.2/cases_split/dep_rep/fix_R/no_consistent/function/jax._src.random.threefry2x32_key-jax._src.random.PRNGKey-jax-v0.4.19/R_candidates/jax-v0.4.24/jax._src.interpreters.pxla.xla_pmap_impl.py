def xla_pmap_impl(fun: lu.WrappedFun, *args, **params):
  compiled_fun = xla_pmap_impl_lazy(fun, *args, **params)
  return compiled_fun(*args)
