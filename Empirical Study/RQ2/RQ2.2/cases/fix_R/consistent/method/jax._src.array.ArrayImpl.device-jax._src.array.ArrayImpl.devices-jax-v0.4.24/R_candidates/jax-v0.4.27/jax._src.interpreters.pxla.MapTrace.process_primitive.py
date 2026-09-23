  def process_primitive(self, primitive, tracers, params):
    info = self.main.payload["emap_info"]
    vals, shard_axes = unzip2([(t.val, t.shard_axes) for t in tracers])
    names = tuple(f.name for f in core.thread_local_state.trace_state.axis_env
                  if f.main_trace is self.main)
    all_axes = tuple(_map_schedule(map(s.get, names)) for s in shard_axes)  # pytype: disable=wrong-arg-types  # always-use-return-annotations
    f = HashableFunction(lambda *args: primitive.bind(*args, **params),
                         (primitive, tuple(params.items())))
    f_mapped, out_shard_axes = _multi_pmap(f, info, names, all_axes)
    with core.eval_context(), jax.disable_jit(False):
      outvals = f_mapped(*vals)
    if primitive.multiple_results:
      return [MapTracer(self, val, out_shard_axes) for val in outvals]
    return MapTracer(self, outvals, out_shard_axes)
