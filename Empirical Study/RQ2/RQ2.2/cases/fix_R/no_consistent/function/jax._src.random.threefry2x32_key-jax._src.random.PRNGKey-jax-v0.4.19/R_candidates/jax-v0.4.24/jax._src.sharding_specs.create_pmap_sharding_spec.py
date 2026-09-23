def create_pmap_sharding_spec(shape: tuple[int, ...], sharded_dim: int = 0,
                              sharded_dim_size: int | None = None):
  if sharded_dim is not None:
    if config.pmap_no_rank_reduction.value:
      sharded_shape = util.tuple_update(shape, sharded_dim, 1)
    else:
      sharded_shape = util.tuple_delete(shape, sharded_dim)
    if sharded_dim_size is None:
      sharded_dim_size = shape[sharded_dim]
  else:
    assert sharded_dim_size is not None
    sharded_shape = shape

  return pmap_sharding_spec(sharded_dim_size, sharded_dim_size, sharded_shape,
                            sharded_dim)
