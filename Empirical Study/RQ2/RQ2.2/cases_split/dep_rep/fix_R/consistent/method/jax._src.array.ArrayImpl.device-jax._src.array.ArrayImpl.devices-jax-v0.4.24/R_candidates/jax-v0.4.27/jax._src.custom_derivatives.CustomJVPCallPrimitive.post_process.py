  def post_process(self, trace, out_tracers, jvp_was_run: bool):
    return trace.post_process_custom_jvp_call(out_tracers, jvp_was_run)
