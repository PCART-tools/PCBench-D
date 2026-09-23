  def __eq__(self, other):
    return (self.partitions == other.partitions and
            self.sync == other.sync)
