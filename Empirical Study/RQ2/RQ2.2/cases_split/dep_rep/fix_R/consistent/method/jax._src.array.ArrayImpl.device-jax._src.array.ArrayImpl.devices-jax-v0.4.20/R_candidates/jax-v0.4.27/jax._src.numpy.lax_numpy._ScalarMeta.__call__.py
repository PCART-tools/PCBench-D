  def __call__(self, x: Any) -> Array:
    return asarray(x, dtype=self.dtype)
