  def __instancecheck__(self, instance: Any) -> bool:
    return isinstance(instance, self.dtype.type)
