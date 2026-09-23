  def __init__(self, child: Doc):
    assert isinstance(child, Doc), child
    self.child = child
