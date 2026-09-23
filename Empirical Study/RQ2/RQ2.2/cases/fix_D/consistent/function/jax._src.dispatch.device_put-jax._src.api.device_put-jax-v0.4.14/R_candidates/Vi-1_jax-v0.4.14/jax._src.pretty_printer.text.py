def text(s: str, annotation: Optional[str] = None) -> Doc:
  """Literal text."""
  return _TextDoc(s, annotation)
