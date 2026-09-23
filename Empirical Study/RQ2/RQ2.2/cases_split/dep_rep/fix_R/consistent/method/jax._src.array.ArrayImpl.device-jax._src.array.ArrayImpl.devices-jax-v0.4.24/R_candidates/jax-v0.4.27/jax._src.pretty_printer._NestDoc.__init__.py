  def __init__(self, n: int, child: Doc):
    assert isinstance(child, Doc), child
    self.n = n
    self.child = child
