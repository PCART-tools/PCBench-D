  def __init__(self, tracer: core.Tracer):
    JAXTypeError.__init__(self,
        f"Attempted boolean conversion of {tracer._error_repr()}."
        f"{tracer._origin_msg()}")
