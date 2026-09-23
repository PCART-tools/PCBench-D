  @classmethod
  def tree_unflatten(cls, keys, values):
    return _DictWrapper(keys, values)
