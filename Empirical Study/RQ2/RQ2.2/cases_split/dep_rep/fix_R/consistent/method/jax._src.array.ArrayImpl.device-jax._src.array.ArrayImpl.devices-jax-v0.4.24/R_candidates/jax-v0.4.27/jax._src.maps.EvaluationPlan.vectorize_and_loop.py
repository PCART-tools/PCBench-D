  def vectorize_and_loop(self, f: lu.WrappedFun, in_axes, out_axes) -> lu.WrappedFun:
    vmap_axes = {
        naxis: raxes[-1]
        for naxis, raxes in self.axis_subst_dict.items()
        if self.axis_vmap_size[naxis] is not None
    }
    for naxis, vaxis in sorted(vmap_axes.items(), key=lambda x: x[1].uid):
      local_tile_size = self.axis_vmap_size[naxis]
      map_in_axes = tuple(unsafe_map(lambda spec: spec.get(naxis, None), in_axes))
      map_out_axes = tuple(unsafe_map(lambda spec: spec.get(naxis, None), out_axes))
      f = batching.vtile(f, map_in_axes, map_out_axes, tile_size=local_tile_size, axis_name=vaxis)

    used_loops = set(it.chain.from_iterable(self.loop_axis_resources.values()))
    if not used_loops:
      return f

    if len(used_loops) > 1:
      # TODO: Support multiple loops
      raise NotImplementedError("Only one loop per xmap is supported")
    loop_in_axes = _to_resource_axes(in_axes, self.loop_axis_resources)
    loop_out_axes = _to_resource_axes(out_axes, self.loop_axis_resources)
    loop_name, = used_loops
    loop_length = self.resource_env.shape[loop_name]
    def looped_f(*args):
      def body(i, _):
        # XXX: This call_wrapped is only valid under the assumption that scan
        #      only ever traces the body once (which it does at the moment).
        result = f.call_wrapped(
            *(_slice_tile(arg, spec.get(loop_name, None), i, loop_length)
              for arg, spec in zip(args, loop_in_axes)))
        return i + 1, result
      _, stacked_results = lax.scan(body, 0, (), length=loop_length)
      return [_merge_leading_axis(sresult, spec.get(loop_name, None))
              for sresult, spec in zip(stacked_results, loop_out_axes)]
    return lu.wrap_init(looped_f)
