  def __hash__(self):
    return hash(tuple((k, v) for k, v in sorted(self.val.items())))
