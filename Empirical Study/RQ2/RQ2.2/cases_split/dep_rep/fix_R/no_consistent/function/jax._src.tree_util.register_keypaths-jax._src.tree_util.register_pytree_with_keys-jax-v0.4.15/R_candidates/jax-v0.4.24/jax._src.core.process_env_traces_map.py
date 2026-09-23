@lu.transformation_with_aux
def process_env_traces_map(primitive: MapPrimitive, level: int,
                           params_tuple: tuple, *args):
  outs = yield args, {}
  params = dict(params_tuple)
  todo = []
  out_axes_transforms = []
  while True:
    tracers = [x for x in outs if isinstance(x, Tracer)
               and (level is None or x._trace.level > level)]
    if not tracers:
      break
    ans = max(tracers, key=operator.attrgetter('_trace.level'))
    trace = ans._trace.main.with_cur_sublevel()
    outs = map(trace.full_raise, outs)
    outs, (cur_todo, cur_xform) = primitive.post_process(trace, outs, params)
    todo.append(cur_todo)
    out_axes_transforms.append(cur_xform)
  yield outs, (tuple(todo), tuple(out_axes_transforms))
