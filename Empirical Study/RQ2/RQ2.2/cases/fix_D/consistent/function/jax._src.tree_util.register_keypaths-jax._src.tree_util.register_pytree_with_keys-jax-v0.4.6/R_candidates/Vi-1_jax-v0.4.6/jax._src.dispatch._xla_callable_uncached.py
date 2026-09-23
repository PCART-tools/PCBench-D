def _xla_callable_uncached(fun: lu.WrappedFun, device, backend, name,
                           donated_invars, keep_unused, *arg_specs):
  if config.jax_array:
    computation = sharded_lowering(fun, device, backend, name, donated_invars,
                                   False, keep_unused, *arg_specs,
                                   lowering_platform=None)
    allow_prop = [True] * len(computation.compile_args['global_out_avals'])
    return computation.compile(_allow_propagation_to_outputs=allow_prop).unsafe_call
  else:
    return lower_xla_callable(fun, device, backend, name, donated_invars, False,
                              keep_unused, *arg_specs,
                              lowering_platform=None).compile().unsafe_call
