  def __init__(self, traceback_info, fmt_string, *a, **k):
    super().__init__(traceback_info)
    self.fmt_string = fmt_string
    self.args = a
    self.kwargs = k
