  def post_process_custom_vjp_call(self, out_tracers, _):
    raise CustomVJPException()
