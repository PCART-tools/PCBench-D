  def post_process_call(self, call_primitive, out_tracers, params):
    primals, tangents = unzip2((t.primal, t.tangent) for t in out_tracers)
    out, treedef = tree_flatten((primals, tangents))
    tangents_nz = [type(t) is not Zero for t in tangents]
    del primals, tangents
    main = self.main
    def todo(x):
      primals, tangents = tree_unflatten(treedef, x)
      trace = JVPTrace(main, core.cur_sublevel())
      return map(partial(JVPTracer, trace), primals, tangents)
    if call_primitive.map_primitive:
      def out_axes_transform(out_axes):
        return (*out_axes, *(ax for ax, nz in zip(out_axes, tangents_nz) if nz))
      todo = (todo, out_axes_transform)
    return out, todo
