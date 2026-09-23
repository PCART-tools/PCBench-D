def map_bind_with_continuation(primitive: MapPrimitive, fun, *args,
                               out_axes_thunk, **params):
  # The new thunk depends deterministically on the old thunk and the wrapped
  # function. Any caching already has to include the wrapped function as part
  # of the key, so we only use the previous thunk for equality checks.
  @as_hashable_function(closure=out_axes_thunk)
  def new_out_axes_thunk():
    out_axes = out_axes_thunk()
    _, out_axes_transforms = todo_and_xforms()
    for t in out_axes_transforms:
      out_axes = t(out_axes)
    return out_axes
  params = dict(params, out_axes_thunk=new_out_axes_thunk)
  top_trace = find_top_trace(args)
  fun, todo_and_xforms = process_env_traces_map(
      fun, primitive, top_trace and top_trace.level, tuple(params.items()))
  tracers = map(top_trace.full_raise, args)

  def map_bind_continuation(outs):
    env_trace_todo, _ = todo_and_xforms()
    return map(full_lower, apply_todos(env_trace_todo, outs))

  return map_bind_continuation, top_trace, fun, tracers, params
