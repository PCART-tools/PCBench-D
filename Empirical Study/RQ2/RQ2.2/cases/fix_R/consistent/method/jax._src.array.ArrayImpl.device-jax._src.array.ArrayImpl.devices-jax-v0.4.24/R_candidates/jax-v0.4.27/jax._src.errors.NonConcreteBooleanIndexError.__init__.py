  def __init__(self, tracer: core.Tracer):
    super().__init__(
        f"Array boolean indices must be concrete; got {tracer}\n")
