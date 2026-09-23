def text(s: str, annotation: str | None = None) -> Doc:
  """Literal text."""
  return _TextDoc(s, annotation)
