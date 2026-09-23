def _xla_call_impl_lazy(fun: lu.WrappedFun, *args, device, backend, name,
                        donated_invars, inline, keep_unused: bool):
  del inline  # Only used at tracing time
  if fun.in_type is None:
    arg_specs: Iterable[Any] = unsafe_map(arg_spec, args)
  else:
    # fun.in_type is used for dynamic shapes.
    if config.jax_array:
      raise NotImplementedError('Dynamic shapes do not work with Array.')
    arg_specs = [(None, getattr(x, '_device', None)) for x in args]
  return xla_callable(fun, device, backend, name, donated_invars, keep_unused,
                      *arg_specs)
