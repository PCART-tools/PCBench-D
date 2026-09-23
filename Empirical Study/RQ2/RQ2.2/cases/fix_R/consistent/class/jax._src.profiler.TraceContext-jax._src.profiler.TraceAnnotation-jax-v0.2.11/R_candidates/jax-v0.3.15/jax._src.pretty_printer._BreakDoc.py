class _BreakDoc(Doc):
  __slots__ = ("text",)
  text: str

  def __init__(self, text: str):
    assert isinstance(text, str), text
    self.text = text

  def __repr__(self): return f"break({self.text})"
