@lu.transformation_with_aux
def batch_custom_jvp_subtrace(main, in_dims, *in_vals):
  size, = {x.shape[d] for x, d in zip(in_vals, in_dims * 2)
           if d is not not_mapped}
  trace = main.with_cur_sublevel()
  in_tracers = [val if dim is None else
                SymbolicZero(core.mapped_aval(size, dim, val.aval))
                if type(val) is SymbolicZero else BatchTracer(trace, val, dim)
                for val, dim in zip(in_vals, in_dims * 2)]
  outs = yield in_tracers, {}
  # TODO(mattjj,frostig): instantiating any SymbolicZero output is easy, but can
  # be wasteful in the rare case it actually triggers; handle symbolically!
  outs = [instantiate(replace_rule_output_symbolic_zeros(x)) for x in outs]
  out_tracers = map(trace.full_raise, outs)
  out_vals, out_dims = unzip2((t.val, t.batch_dim) for t in out_tracers)
  out_primals, out_tangents = split_list(out_vals, [len(out_vals) // 2])
  out_primal_bds, out_tangent_bds = split_list(out_dims, [len(out_vals) // 2])
  out_dims = map(_merge_bdims, out_primal_bds, out_tangent_bds)
  out_primals  = map(partial(matchaxis, trace.axis_name, size),
                     out_primal_bds, out_dims,  out_primals)
  out_tangents = map(partial(matchaxis, trace.axis_name, size),
                     out_tangent_bds, out_dims, out_tangents)
  yield out_primals + out_tangents, out_dims * 2
