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
