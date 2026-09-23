  @property
  def addressable_shards(self) -> list[Shard]:
    return [
        type(s)(
            device=s._device,
            sharding=s._sharding,
            global_shape=s._global_shape,
            data=PRNGKeyArray(self._impl, s._data),
        )
        for s in self._base_array.addressable_shards
    ]
