@lu.transformation_with_aux
def _match_axes_jaxpr(axis_size, out_axes_dest, out_axes, main, in_axes,
                      *in_vals):
  trace = main.with_cur_sublevel()
  out_vals = yield (main, in_axes, *in_vals), {}
  out_axes = out_axes()
  out_axes_dest = [(None if src is not_mapped else 0)
                   if dst is zero_if_mapped else dst
                   for src, dst in unsafe_zip(out_axes, out_axes_dest)]
  if len(out_axes_dest) != len(out_axes):
    out_axis_dest, = out_axes_dest
    out_axes_dest = [out_axis_dest] * len(out_axes)
  out_vals = map(partial(matchaxis, trace.axis_name, axis_size),
                 out_axes, out_axes_dest, out_vals)
  out_batched = [dst is not None for dst in out_axes_dest]
  yield out_vals, out_batched
