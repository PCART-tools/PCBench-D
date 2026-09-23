def brk(text: str = " ") -> Doc:
  """A break.

  Prints either as a newline or as `text`, depending on the enclosing group.
  """
  return _BreakDoc(text)
