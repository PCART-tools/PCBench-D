class CallPrimitive(Primitive):
  multiple_results = True
  call_primitive = True

  def bind(self, fun, *args, **params):
    call_bind_continuation, top_trace, fun_, tracers, params = (
        call_bind_with_continuation(self, fun, *args, **params))
    outs = top_trace.process_call(self, fun_, tracers, params)
    return call_bind_continuation(outs)

  def get_bind_params(self, params):
    new_params = dict(params)
    jaxpr = new_params.pop('call_jaxpr')
    subfun = lu.hashable_partial(lu.wrap_init(eval_jaxpr), jaxpr, ())
    if config.dynamic_shapes.value:
      subfun = lu.annotate(subfun, _jaxpr_type_to_callable_annotation(jaxpr))
    return [subfun], new_params
