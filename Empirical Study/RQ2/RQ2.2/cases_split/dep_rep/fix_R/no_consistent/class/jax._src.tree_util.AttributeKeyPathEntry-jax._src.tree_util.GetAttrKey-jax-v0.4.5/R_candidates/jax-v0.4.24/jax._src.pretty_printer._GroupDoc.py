class _GroupDoc(Doc):
  __slots__ = ("child",)
  child: Doc

  def __init__(self, child: Doc):
    assert isinstance(child, Doc), child
    self.child = child

  def __repr__(self): return f"group({self.child})"
