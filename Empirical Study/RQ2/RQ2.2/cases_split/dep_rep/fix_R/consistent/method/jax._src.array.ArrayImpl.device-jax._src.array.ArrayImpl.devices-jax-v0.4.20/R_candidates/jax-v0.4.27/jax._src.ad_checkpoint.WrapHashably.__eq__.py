  def __eq__(self, other):
    if isinstance(other, WrapHashably):
      if self.hashable and other.hashable:
        return self.val == other.val
      else:
        return self.val is other.val
    return False
