def _sda_addressable_shards(self):
  from jax._src import array
  out = []
  for db in self.device_buffers:
    db = dispatch._set_aval(db)
    out.append(array.Shard(db.device(), self.sharding, self.shape, db))
  return out
