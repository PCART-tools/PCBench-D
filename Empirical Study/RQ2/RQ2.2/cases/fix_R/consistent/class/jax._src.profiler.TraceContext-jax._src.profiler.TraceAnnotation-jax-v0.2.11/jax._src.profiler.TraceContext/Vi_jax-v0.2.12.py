class TraceContext(TraceAnnotation):
  def __init__(self, *args, **kwargs):
    warnings.warn(
        "TraceContext has been renamed to TraceAnnotation. This alias "
        "will eventually be removed; please update your code.")
    super().__init__(*args, **kwargs)
