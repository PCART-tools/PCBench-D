  def __new__(cls, *partitions):
    return tuple.__new__(PartitionSpec, partitions)
