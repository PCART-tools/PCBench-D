  def process_call(self, call_primitive, f, tracers, params):
    assert call_primitive.multiple_results
    primals, tangents = unzip2((t.primal, t.tangent) for t in tracers)
    which_nz = [     type(t) is not Zero           for t in tangents]
    tangents = [t if type(t) is not Zero else None for t in tangents]
    args, in_tree = tree_flatten((primals, tangents))
    f_jvp = jvp_subtrace(f, self.main)
    f_jvp, which_nz_out = nonzero_tangent_outputs(f_jvp)
    if isinstance(call_primitive, core.MapPrimitive):
      in_axes = params['in_axes']
      tangent_in_axes = [ax for ax, nz in zip(in_axes, which_nz) if nz]
      out_axes_thunk = params['out_axes_thunk']
      # NOTE: This assumes that the output tangents being zero is a
      # deterministic function of which input tangents were zero.
      @as_hashable_function(closure=out_axes_thunk)
      def new_out_axes_thunk():
        out_ax = out_axes_thunk()
        return (*out_ax, *(ax for ax, nz in zip(out_ax, which_nz_out()) if nz))
      params = dict(params, in_axes=(*in_axes, *tangent_in_axes),
                    out_axes_thunk=new_out_axes_thunk)
    f_jvp, out_tree = traceable(f_jvp, in_tree)
    update_params = call_param_updaters.get(call_primitive)
    new_params = update_params(params, which_nz) if update_params else params
    result = call_primitive.bind(_update_annotation(f_jvp, f.in_type, which_nz),
                                 *args, **new_params)
    primal_out, tangent_out = tree_unflatten(out_tree(), result)
    tangent_out = [Zero(get_aval(p).at_least_vspace()) if t is None else t
                   for p, t in zip(primal_out, tangent_out)]
    return [JVPTracer(self, p, t) for p, t in zip(primal_out, tangent_out)]
