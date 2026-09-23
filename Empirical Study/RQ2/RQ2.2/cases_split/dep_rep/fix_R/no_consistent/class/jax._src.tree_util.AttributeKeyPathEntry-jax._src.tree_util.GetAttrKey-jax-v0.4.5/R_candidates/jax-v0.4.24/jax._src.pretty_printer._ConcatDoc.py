class _ConcatDoc(Doc):
  __slots__ = ("children",)
  children: list[Doc]

  def __init__(self, children: Sequence[Doc]):
    self.children = list(children)
    assert all(isinstance(doc, Doc) for doc in self.children), self.children

  def __repr__(self): return f"concat({self.children})"
