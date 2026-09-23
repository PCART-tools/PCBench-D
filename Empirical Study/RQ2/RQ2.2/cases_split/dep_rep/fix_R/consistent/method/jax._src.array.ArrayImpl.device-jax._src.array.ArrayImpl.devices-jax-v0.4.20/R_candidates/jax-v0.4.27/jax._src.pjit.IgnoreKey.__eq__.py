  def __eq__(self, other):
    return isinstance(other, IgnoreKey)  # ignore self.val!
