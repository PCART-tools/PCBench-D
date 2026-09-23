  def __init__(self, tracer: core.Tracer):
    super().__init__(
        f"The __index__() method was called on {tracer._error_repr()}"
        f"{tracer._origin_msg()}")
