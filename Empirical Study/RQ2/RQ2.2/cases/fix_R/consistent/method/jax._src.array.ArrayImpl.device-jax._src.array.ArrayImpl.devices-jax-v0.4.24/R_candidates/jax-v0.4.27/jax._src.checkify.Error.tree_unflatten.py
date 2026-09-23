  @classmethod
  def tree_unflatten(cls, metadata, data):
    pred, code, payload = data
    return cls(pred, code, metadata, payload)
