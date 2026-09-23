  def __eq__(self, other):
    return type(self.val) is type(other.val) and self.val == other.val
