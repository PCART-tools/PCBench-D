  def get_referent(self):
    frame = self._trace.frame
    val = frame.constvar_to_val.get(frame.tracer_to_var.get(id(self)))
    return self if val is None else get_referent(val)
