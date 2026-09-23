class _NestDoc(Doc):
  __slots__ = ("n", "child",)
  n: int
  child: Doc

  def __init__(self, n: int, child: Doc):
    assert isinstance(child, Doc), child
    self.n = n
    self.child = child

  def __repr__(self): return f"nest({self.n, self.child})"
