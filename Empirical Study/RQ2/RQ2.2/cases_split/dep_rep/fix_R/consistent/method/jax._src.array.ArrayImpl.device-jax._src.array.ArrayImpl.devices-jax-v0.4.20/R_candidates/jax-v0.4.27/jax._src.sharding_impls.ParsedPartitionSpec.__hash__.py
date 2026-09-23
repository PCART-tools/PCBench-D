  def __hash__(self):
    return hash((self.partitions, self.sync))
