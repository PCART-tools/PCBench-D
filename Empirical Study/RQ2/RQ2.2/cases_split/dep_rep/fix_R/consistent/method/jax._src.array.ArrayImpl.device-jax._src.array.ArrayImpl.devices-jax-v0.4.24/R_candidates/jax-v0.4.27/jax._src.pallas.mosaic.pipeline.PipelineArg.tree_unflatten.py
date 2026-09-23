  @classmethod
  def tree_unflatten(cls, _, children):
    return cls(*children)
