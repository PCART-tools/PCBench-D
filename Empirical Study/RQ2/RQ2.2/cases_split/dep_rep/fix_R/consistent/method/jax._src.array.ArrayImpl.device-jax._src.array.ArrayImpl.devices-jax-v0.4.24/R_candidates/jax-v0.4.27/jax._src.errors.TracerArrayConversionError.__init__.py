  def __init__(self, tracer: core.Tracer):
    super().__init__(
        "The numpy.ndarray conversion method __array__() was called on "
        f"{tracer._error_repr()}{tracer._origin_msg()}")
