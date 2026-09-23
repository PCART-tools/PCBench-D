  def shard_shape(self, global_shape: Shape) -> Shape:
    return _common_shard_shape(self, global_shape)
