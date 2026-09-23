def wrap_with_sharding_op(x: ir.Value,
                          sharding_proto: xc.OpSharding,
                          unspecified_dims: Optional[Set[int]] = None):
  return _wrap_with_spmd_op("Sharding", x.type, x, sharding_proto,
                            unspecified_dims)
