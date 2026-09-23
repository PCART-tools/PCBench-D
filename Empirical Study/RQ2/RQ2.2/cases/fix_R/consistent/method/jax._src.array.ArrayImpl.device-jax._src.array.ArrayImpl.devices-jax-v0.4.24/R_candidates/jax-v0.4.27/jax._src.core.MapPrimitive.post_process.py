  def post_process(self, trace, out_tracers, params):
    return trace.post_process_map(self, out_tracers, params)
