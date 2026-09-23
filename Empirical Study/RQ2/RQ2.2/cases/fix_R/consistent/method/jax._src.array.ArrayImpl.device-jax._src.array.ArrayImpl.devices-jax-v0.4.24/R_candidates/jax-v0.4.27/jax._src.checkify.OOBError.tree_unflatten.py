  @classmethod
  def tree_unflatten(cls, metadata, payload):
    return cls(*metadata, payload[0])
