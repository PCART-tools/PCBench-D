  def shard_shape(self, global_shape: Shape) -> Shape:
    """Returns the shape of the data on each device.

    The shard shape returned by this function is calculated from
    ``global_shape`` and the properties of the sharding.
    """
    raise NotImplementedError('Subclasses should implement this method.')
