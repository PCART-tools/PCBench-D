  def process_custom_jvp_call(self, primitive, fun, jvp, tracers, *,
                              symbolic_zeros):
    msg = (f"{type(self)} must override process_custom_jvp_call "
           "to handle custom_jvp primitives")
    raise NotImplementedError(msg)
