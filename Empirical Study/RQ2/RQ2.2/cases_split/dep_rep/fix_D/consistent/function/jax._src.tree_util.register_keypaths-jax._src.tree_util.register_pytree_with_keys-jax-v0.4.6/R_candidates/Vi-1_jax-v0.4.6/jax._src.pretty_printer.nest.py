def nest(n: int, doc: Doc) -> Doc:
  """Increases the indentation level by `n`."""
  return _NestDoc(n, doc)
