  def __hash__(self):
    return hash((self.device_local_layout, self.sharding))
