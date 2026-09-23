  def __init__(self, shape, dtype, weak_type=False, named_shape=None):
    self.shape = canonicalize_shape(shape)
    self.dtype = _dtype_object(dtype)
    self.weak_type = weak_type
    self.named_shape = {} if named_shape is None else dict(named_shape)
