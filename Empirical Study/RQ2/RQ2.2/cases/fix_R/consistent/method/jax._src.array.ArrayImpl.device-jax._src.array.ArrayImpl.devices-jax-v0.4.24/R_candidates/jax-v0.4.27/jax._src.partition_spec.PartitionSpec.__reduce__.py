  def __reduce__(self):
    return (PartitionSpec, tuple(self))
