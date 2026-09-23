  def __eq__(self, other):
    return type(other) is _UniqueResourceName and self.uid == other.uid
