@lu.transformation_with_aux
def _batch_jaxpr_inner(axis_size, main, in_axes, *in_vals):
  trace = main.with_cur_sublevel()
  in_tracers = [BatchTracer(trace, val, dim) if dim is not None else val
                for val, dim in zip(in_vals, in_axes)]
  outs = yield in_tracers, {}
  out_tracers = map(trace.full_raise, outs)
  out_vals, out_axes = unzip2((t.val, t.batch_dim) for t in out_tracers)
  yield out_vals, out_axes
