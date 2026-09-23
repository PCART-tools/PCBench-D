  @staticmethod
  def full(shape, fill_value, dtype):
    physical_shape = (*shape, *dtype._impl.key_shape)
    if hasattr(fill_value, 'dtype') and jnp.issubdtype(fill_value.dtype, dtypes.prng_key):
      key_data = jnp.broadcast_to(random_unwrap(fill_value), physical_shape)
    else:
      key_data = lax.full(physical_shape, fill_value, dtype=np.dtype('uint32'))
    # TODO(frostig,mattjj,vanderplas,lenamartens): consider this consumed from
    # the outset.
    return random_wrap(key_data, impl=dtype._impl)
