  def __getitem__(self, key: slice | tuple[slice, ...]) -> Array:
    if isinstance(key, slice):
      return _make_1d_grid_from_slice(key, op_name="mgrid")
    output: Iterable[Array] = (_make_1d_grid_from_slice(k, op_name="mgrid") for k in key)
    with jax.numpy_dtype_promotion('standard'):
      output = promote_dtypes(*output)
    output_arr = meshgrid(*output, indexing='ij', sparse=False)
    if len(output_arr) == 0:
      return arange(0)
    return stack(output_arr, 0)
