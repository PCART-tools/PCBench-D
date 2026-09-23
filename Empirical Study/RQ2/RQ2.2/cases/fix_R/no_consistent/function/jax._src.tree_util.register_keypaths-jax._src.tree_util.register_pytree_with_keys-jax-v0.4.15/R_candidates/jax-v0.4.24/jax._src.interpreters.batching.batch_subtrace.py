@lu.transformation_with_aux
def batch_subtrace(main, in_dims, *in_vals):
  trace = main.with_cur_sublevel()
  in_dims = in_dims() if callable(in_dims) else in_dims
  in_vals, in_dims = resolve_ragged_axes(in_vals, in_dims)
  in_tracers = [BatchTracer(trace, x, dim, source_info_util.current())
                if dim is not None else x for x, dim in zip(in_vals, in_dims)]
  outs = yield in_tracers, {}
  out_tracers = map(trace.full_raise, outs)
  out_vals, out_dims = unzip2((t.val, t.batch_dim) for t in out_tracers)
  segment_lens, out_dims = indirectify_ragged_axes(out_dims)
  yield (*segment_lens, *out_vals), out_dims
