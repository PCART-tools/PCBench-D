  @classmethod
  def tree_unflatten(cls, metadata, payload):
    del payload
    return cls(metadata)
