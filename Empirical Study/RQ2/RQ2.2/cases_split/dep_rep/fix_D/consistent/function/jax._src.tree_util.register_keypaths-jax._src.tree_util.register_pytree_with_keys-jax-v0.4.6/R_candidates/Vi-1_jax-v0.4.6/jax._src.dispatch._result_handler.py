def _result_handler(backend: Backend,
                    sticky_device: Optional[Device],
                    out_type: pe.OutputType,
                    ) -> Callable:
  out_avals, kept_outputs = util.unzip2(out_type)
  handlers = map(partial(aval_to_result_handler, sticky_device), out_avals)
  dyn_outs = any(type(aval) is core.DShapedArray and
                 any(type(d) in (core.InDBIdx, core.OutDBIdx) for d in aval.shape)
                 for aval in out_avals)
  if not dyn_outs:
    return SimpleResultHandler(handlers)
  assert config.jax_dynamic_shapes

  def result_handler(input_env, lists_of_bufs):
    results = []
    for handler, bufs in unsafe_zip(handlers, lists_of_bufs):
      results.append(handler((input_env, results), *bufs))
    return [r for r, keep in unsafe_zip(results, kept_outputs) if keep]
  return result_handler
