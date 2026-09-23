  def __eq__(self, other):
    if not isinstance(other, Layout):
      return False
    return (self.device_local_layout == other.device_local_layout and
            self.sharding == other.sharding)
