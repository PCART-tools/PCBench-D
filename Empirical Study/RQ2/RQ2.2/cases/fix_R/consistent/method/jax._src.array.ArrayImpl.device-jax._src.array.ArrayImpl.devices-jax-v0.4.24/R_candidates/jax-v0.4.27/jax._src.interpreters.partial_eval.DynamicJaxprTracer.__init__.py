  def __init__(self, trace, aval, line_info=None):
    self._trace = trace
    self._line_info = line_info
    # Needed for UnexpectedTracerError.
    self._debug_info = self._trace.frame.debug_info
    self.aval = aval
