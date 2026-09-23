  def __init__(self, dtype, val, weak_type=None):
    super().__init__(
        np.shape(val), dtype,
        weak_type=dtypes.is_weakly_typed(val) if weak_type is None else weak_type)
    dtypes.check_valid_dtype(self.dtype)
    # Note: canonicalized self.dtype doesn't necessarily match self.val
    assert self.dtype == dtypes.canonicalize_dtype(np.result_type(val)), (val, dtype)
    self.val = val
