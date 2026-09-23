  def addressable_shards(self):
    from jax._src import array
    return [array.Shard(self.device(), self.sharding, self.shape,
                        self.device_buffer)]
