def vmap_unrestricted(f: lu.WrappedFun, *args, in_axes, axis_name, axis_size):
  f, out_axes = batching.batch_subtrace(f)
  f = batching._batch_outer(f, axis_name, axis_size, in_axes,
                            batching.BatchTrace, None)
  outs = f.call_wrapped(*args)
  return outs, out_axes()
