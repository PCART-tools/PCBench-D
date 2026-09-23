  def post_process(self, trace, out_tracers, params):
    return trace.post_process_custom_vjp_call(out_tracers, params)
