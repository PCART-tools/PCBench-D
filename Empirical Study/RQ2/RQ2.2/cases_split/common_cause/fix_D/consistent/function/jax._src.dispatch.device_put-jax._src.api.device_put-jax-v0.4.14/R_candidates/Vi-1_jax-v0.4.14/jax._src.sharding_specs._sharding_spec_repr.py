def _sharding_spec_repr(self):
  return f'ShardingSpec({self.sharding}, {self.mesh_mapping})'
