  def __getitem__(
      self, key: slice | tuple[slice, ...]
  ) -> Array | list[Array]:
    if isinstance(key, slice):
      return _make_1d_grid_from_slice(key, op_name="ogrid")
    output: Iterable[Array] = (_make_1d_grid_from_slice(k, op_name="ogrid") for k in key)
    with jax.numpy_dtype_promotion('standard'):
      output = promote_dtypes(*output)
    return meshgrid(*output, indexing='ij', sparse=True)
