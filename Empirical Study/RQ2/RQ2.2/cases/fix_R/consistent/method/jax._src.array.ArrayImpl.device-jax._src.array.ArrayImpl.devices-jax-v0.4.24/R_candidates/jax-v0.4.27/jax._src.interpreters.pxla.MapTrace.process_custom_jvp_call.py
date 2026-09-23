  def process_custom_jvp_call(self, prim, fun, jvp, tracers, *, symbolic_zeros):
    if symbolic_zeros:
      msg = ("custom_jvp with symbolic_zeros=True not supported with eager pmap. "
             "Please open an issue at https://github.com/google/jax/issues !")
      raise NotImplementedError(msg)
    del prim, jvp, symbolic_zeros  # always base main, can drop jvp
    in_vals, in_axes = unzip2((t.val, t.shard_axes) for t in tracers)
    fun, out_axes = _emap_subtrace(fun, self.main, in_axes)
    with core.new_sublevel():
      out_vals = fun.call_wrapped(*in_vals)
    return map(partial(MapTracer, self), out_vals, out_axes())
