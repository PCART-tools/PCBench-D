  def __repr__(self):
    ns = f", named_shape={self.named_shape}" if self.named_shape else ""
    sh = f", sharding={self.sharding}" if self.sharding is not None else ""
    l = f", layout={self.layout}" if self._dll is not None else ""
    return (f"{type(self).__name__}(shape={self.shape}, "
            f"dtype={self.dtype.name}{ns}{sh}{l})")
