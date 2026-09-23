  def __init__(self, children: Sequence[Doc]):
    self.children = list(children)
    assert all(isinstance(doc, Doc) for doc in self.children), self.children
