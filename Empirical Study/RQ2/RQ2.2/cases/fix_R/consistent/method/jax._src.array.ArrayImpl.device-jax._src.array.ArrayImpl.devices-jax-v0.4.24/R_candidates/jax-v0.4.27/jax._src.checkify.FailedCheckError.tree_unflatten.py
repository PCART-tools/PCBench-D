  @classmethod
  def tree_unflatten(cls, metadata, payload):
    args, kwargs = payload
    return cls(*metadata, *args, **kwargs)
