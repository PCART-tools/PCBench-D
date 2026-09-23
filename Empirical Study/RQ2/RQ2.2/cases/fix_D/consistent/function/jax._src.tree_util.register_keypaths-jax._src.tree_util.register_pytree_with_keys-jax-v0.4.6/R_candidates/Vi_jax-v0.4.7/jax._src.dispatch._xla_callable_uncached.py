def _xla_callable_uncached(fun: lu.WrappedFun, name, donated_invars,
                           keep_unused, *arg_specs):
  computation = sharded_lowering(fun, name, donated_invars, keep_unused,
                                 *arg_specs, lowering_platform=None)
  allow_prop = [True] * len(computation.compile_args['global_out_avals'])
  return computation.compile(_allow_propagation_to_outputs=allow_prop).unsafe_call
