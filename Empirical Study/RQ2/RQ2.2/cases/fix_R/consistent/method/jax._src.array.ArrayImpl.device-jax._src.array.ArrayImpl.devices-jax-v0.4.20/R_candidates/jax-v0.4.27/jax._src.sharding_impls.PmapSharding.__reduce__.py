  def __reduce__(self):
    return (type(self), (self.devices, self.sharding_spec),
            {'memory_kind': self.memory_kind})
