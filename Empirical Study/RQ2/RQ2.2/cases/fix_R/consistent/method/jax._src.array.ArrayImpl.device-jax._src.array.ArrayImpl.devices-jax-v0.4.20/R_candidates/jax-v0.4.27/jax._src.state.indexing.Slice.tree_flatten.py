  def tree_flatten(self):
    # If `start` is statically known, we treat it as static information
    xs = ()
    data = ()
    xs += (self.start,) if self.is_dynamic_start else (None,)
    data += (None,) if self.is_dynamic_start else (self.start,)
    xs += (self.size,) if self.is_dynamic_size else (None,)
    data += (None,) if self.is_dynamic_size else (self.size,)
    data += (self.stride,)
    return xs, data
