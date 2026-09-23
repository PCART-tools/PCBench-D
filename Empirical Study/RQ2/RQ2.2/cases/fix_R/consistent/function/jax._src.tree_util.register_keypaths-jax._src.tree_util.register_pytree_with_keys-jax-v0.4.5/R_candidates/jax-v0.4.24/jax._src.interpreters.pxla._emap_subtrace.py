@lu.transformation_with_aux
def _emap_subtrace(main, in_axes, *in_vals):
  t = main.with_cur_sublevel()
  in_tracers = map(partial(MapTracer, t), in_vals, in_axes)
  ans = yield in_tracers, {}
  out_tracers = map(t.full_raise, ans)
  out_vals, out_axes = unzip2((t.val, t.shard_axes) for t in out_tracers)
  del t, in_tracers, ans, out_tracers
  yield out_vals, out_axes
