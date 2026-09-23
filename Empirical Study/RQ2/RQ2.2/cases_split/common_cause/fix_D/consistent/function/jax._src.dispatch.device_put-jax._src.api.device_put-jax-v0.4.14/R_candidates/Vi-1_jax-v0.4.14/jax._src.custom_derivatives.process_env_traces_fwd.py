@partial(lu.transformation_with_aux, use_eq_store=True)
def process_env_traces_fwd(level: int, out_trees, *args):
  outs = yield args, {}
  todo = []
  bwd_transforms = []
  while True:
    tracers = [x for x in outs if isinstance(x, core.Tracer)
               and (level is None or x._trace.level > level)]
    if tracers:
      ans = max(tracers, key=lambda x: x._trace.level)
    else:
      break
    trace = ans._trace.main.with_cur_sublevel()
    outs = map(trace.full_raise, outs)
    outs, cur_todo, bwd_xform = trace.post_process_custom_vjp_call_fwd(outs, out_trees)
    todo.append(cur_todo)
    bwd_transforms.append(bwd_xform)
  yield outs, (tuple(todo), tuple(bwd_transforms))
