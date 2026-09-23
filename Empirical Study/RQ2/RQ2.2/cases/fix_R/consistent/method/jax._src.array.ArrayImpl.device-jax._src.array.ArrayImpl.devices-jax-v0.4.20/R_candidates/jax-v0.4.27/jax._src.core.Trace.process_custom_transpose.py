  def process_custom_transpose(self, prim, call, tracers, **params):
    msg = (f"{type(self)} must override process_custom_transpose "
           "to handle custom_transpose_call primitives")
    raise NotImplementedError(msg)
