@lu.transformation
def _batch_inner(axis_size, out_dim_dests, main, in_dims, *in_vals):
  in_dims = in_dims() if callable(in_dims) else in_dims
  trace = main.with_cur_sublevel()
  idx = memoize(lambda: BatchTracer(trace, make_iota(axis_size), 0,
                                    source_info_util.current()))
  in_tracers = map(partial(to_elt, trace, idx), in_vals, in_dims)
  outs = yield in_tracers, {}
  out_dim_dests = out_dim_dests() if callable(out_dim_dests) else out_dim_dests
  out_vals = map(partial(from_elt, trace, axis_size), outs, out_dim_dests)
  yield out_vals
