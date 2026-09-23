  def __init__(self, tracer: core.Tracer, context: str = ""):
    super().__init__(
        "Abstract tracer value encountered where concrete value is expected: "
        f"{tracer._error_repr()}\n{context}{tracer._origin_msg()}\n")
