def create_pmap_sharding_spec(shape: tuple[int, ...], sharded_dim: int = 0,
                              sharded_dim_size: Optional[int] = None):
  if sharded_dim is not None:
    sharded_shape = shape[:sharded_dim] + shape[sharded_dim+1:]
    if sharded_dim_size is None:
      sharded_dim_size = shape[sharded_dim]
  else:
    assert sharded_dim_size is not None
    sharded_shape = shape

  return pmap_sharding_spec(sharded_dim_size, sharded_dim_size, sharded_shape,
                            sharded_dim)
