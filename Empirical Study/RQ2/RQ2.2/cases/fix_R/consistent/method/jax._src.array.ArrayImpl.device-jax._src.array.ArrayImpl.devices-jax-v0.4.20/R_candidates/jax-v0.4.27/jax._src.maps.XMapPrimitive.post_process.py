  def post_process(self, trace, out_tracers, params):
    post_process = getattr(trace, 'post_process_xmap', None)
    if post_process is None:
      raise NotImplementedError
    return post_process(self, out_tracers, params)
