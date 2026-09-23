  @functools.cached_property
  def addressable_shards(self) -> Sequence[Shard]:
    self._check_if_deleted()
    out = []
    for a in self._arrays:
      out.append(Shard(_get_device(a), self.sharding, self.shape, a))
    return out
