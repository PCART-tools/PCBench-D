class ShardInfo(NamedTuple):
  sharded_avals: Sequence[core.AbstractValue]
  out_sharded_avals: Sequence[core.ShapedArray]
  global_sharded_avals: Sequence[core.AbstractValue]
  num_local_shards: int
  num_global_shards: int
