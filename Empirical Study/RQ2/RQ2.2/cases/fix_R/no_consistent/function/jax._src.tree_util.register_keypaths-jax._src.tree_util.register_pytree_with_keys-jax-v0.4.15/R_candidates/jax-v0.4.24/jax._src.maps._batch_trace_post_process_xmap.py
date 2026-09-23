def _batch_trace_post_process_xmap(self, primitive, out_tracers, params):
  not_mapped = batching.not_mapped
  BT = batching.BatchTracer
  vals, dims, srcs = unzip3((t.val, t.batch_dim, t.source_info) for t in out_tracers)
  main = self.main
  def todo(vals):
    trace = main.with_cur_sublevel()
    return [BT(trace, v, d if d is not_mapped else _axis_after_insertion(d, oa), s)
            for v, d, oa, s in zip(vals, dims, params['out_axes_thunk'](), srcs)]
  def out_axes_transform(out_axes):
    return tuple(oa if d is not_mapped else
                 _fmap_dims(oa, lambda a, nd=_axis_after_insertion(d, oa): a + (nd <= a))
                 for oa, d in zip(out_axes, dims))
  return vals, (todo, out_axes_transform)
