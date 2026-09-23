  def __init__(self, child: Doc, source: Any):
    assert isinstance(child, Doc), child
    self.child = child
    self.source = source
