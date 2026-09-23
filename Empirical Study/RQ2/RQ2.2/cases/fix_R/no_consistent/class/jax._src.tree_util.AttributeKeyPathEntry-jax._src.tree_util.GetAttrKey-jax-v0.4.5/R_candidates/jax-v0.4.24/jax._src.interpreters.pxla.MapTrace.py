class MapTrace(core.Trace):

  def __init__(self, *args, emap_info):
    super().__init__(*args)
    self.emap_info = emap_info

  def pure(self, val):
    return MapTracer(self, val, {})

  def sublift(self, tracer):
    return MapTracer(self, tracer.val, tracer.shard_axes)

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

  def process_call(self, call_primitive, fun, tracers, params):
    raise NotImplementedError

  def process_map(self, map_primitive, fun, tracers, params):
    if params['devices'] is not None:
      raise ValueError("Nested pmap with explicit devices argument.")
    if not config.disable_jit.value:
      bind = HashableFunction(
          lambda *args, **kwargs: map_primitive.bind(fun, *args, **kwargs),
          (map_primitive, fun))
      fake_primitive = FakePrimitive(multiple_results=True, bind=bind)
      return self.process_primitive(fake_primitive, tracers, params)
    axis_name, in_axes, out_axes_thunk, axis_size = (params["axis_name"],
        params["in_axes"], params["out_axes_thunk"], params["axis_size"])
    vals, shard_axes = unzip2((t.val, t.shard_axes) for t in tracers)
    shard_axes = [{axis_name: _annot_to_flat(np.ndim(v), s.values(), ax), **s}
                  if ax is not None else s
                  for v, ax, s in zip(vals, in_axes, shard_axes)]
    # TODO(mattjj): use _emap_subtrace here?
    with core.new_sublevel(), core.extend_axis_env(axis_name, axis_size, self.main):
      t = self.main.with_cur_sublevel()
      in_tracers = map(partial(MapTracer, t), vals, shard_axes)
      ans = fun.call_wrapped(*in_tracers)
      out_tracers = map(t.full_raise, ans)
      out, outaxes = unzip2((t.val, t.shard_axes) for t in out_tracers)
      del t, in_tracers, ans, out_tracers
    out, outaxes = unzip2(_match_annot(axis_name, axis_size, v, s, dst)
                           for v, s, dst in zip(out, outaxes, out_axes_thunk()))
    return map(partial(MapTracer, self), out, outaxes)

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

  def process_custom_vjp_call(self, primitive, fun, fwd, bwd, tracers,
                              out_trees, symbolic_zeros):
    if symbolic_zeros:
      msg = ("custom_vjp with symbolic_zeros=True not supported with eager pmap. "
             "Please open an issue at https://github.com/google/jax/issues !")
      raise NotImplementedError(msg)
    del primitive, fwd, bwd, out_trees, symbolic_zeros  # always base main, drop vjp
    in_vals, in_axes = unzip2((t.val, t.shard_axes) for t in tracers)
    fun, out_axes = _emap_subtrace(fun, self.main, in_axes)
    with core.new_sublevel():
      out_vals = fun.call_wrapped(*in_vals)
    return map(partial(MapTracer, self), out_vals, out_axes())

  def process_axis_index(self, frame):
    bind = HashableFunction(
        lambda _: jax.lax.axis_index(frame.name),
        (jax.lax.axis_index, frame.name))
    fake_primitive = FakePrimitive(multiple_results=False, bind=bind)
    with core.eval_context():
      range = jax.lax.iota(np.int32, frame.size)
    dummy_tracer = MapTracer(self, range, {frame.name: 0})
    return self.process_primitive(fake_primitive, (dummy_tracer,), {})
