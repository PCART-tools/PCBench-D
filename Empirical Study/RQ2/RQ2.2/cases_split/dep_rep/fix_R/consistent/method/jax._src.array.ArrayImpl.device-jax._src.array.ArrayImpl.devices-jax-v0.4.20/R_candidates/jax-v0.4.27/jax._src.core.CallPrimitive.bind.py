  def bind(self, fun, *args, **params):
    call_bind_continuation, top_trace, fun_, tracers, params = (
        call_bind_with_continuation(self, fun, *args, **params))
    outs = top_trace.process_call(self, fun_, tracers, params)
    return call_bind_continuation(outs)
