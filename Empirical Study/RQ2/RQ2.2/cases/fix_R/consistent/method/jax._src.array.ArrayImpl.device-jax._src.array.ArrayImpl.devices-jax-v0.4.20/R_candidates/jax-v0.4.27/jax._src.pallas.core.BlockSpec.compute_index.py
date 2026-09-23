  def compute_index(self, *args):
    assert self.index_map is not None
    assert self.block_shape is not None
    out = self.index_map(*args)
    if not isinstance(out, tuple):
      out = (out,)
    return out
