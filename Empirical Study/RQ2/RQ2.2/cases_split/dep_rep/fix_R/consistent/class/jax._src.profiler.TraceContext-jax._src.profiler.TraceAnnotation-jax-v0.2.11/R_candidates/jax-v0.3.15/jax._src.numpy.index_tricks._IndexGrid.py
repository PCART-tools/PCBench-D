class _IndexGrid(abc.ABC):
  """Creates multi-dimensional grids of indices."""
  sparse: bool
  op_name: str

  def __getitem__(self, key):
    if isinstance(key, slice):
      return _make_1d_grid_from_slice(key, op_name=self.op_name)
    output = (_make_1d_grid_from_slice(k, op_name=self.op_name) for k in key)
    with jax.numpy_dtype_promotion('standard'):
      output = _promote_dtypes(*output)
    output = meshgrid(*output, indexing='ij', sparse=self.sparse)
    return output if self.sparse else stack(output, 0)
