  def get_frame(self, vals, dims) -> core.AxisEnvFrame:
    if any(d is not not_mapped for d in dims):
      sizes = (x.shape[d] if type(d) is int else d.size
               for x, d in zip(vals, dims) if d is not not_mapped)
      axis_size, = core.dedup_referents(sizes)
    else:
      axis_size = None  # can't be inferred from data
    if self.axis_name is core.no_axis_name:
      assert axis_size is not None  # must be inferable from data
      return core.AxisEnvFrame(self.axis_name, axis_size, self.main)
    frame = core.axis_frame(self.axis_name, self.main)
    assert axis_size is None or axis_size == frame.size, (axis_size, frame.size)
    assert frame.main_trace is self.main
    return frame
