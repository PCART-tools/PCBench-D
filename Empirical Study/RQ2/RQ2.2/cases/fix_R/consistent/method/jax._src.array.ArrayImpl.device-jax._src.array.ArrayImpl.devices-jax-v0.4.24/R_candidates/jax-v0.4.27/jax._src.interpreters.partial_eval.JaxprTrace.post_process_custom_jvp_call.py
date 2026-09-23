  def post_process_custom_jvp_call(self, out_tracers, _):
    # This path should only be reachable if we expose a partial eval API
    # unrelated to autodiff, since we raise an error when differentiation with
    # respect to values over which a custom_jvp function closes is detected.
    raise NotImplementedError  # TODO(mattjj)
