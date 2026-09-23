  @property
  def aval(self):
    aval = raise_to_shaped(core.get_aval(self.val))
    if self.batch_dim is not_mapped:
      return aval
    elif type(self.batch_dim) is int:
      return core.mapped_aval(aval.shape[self.batch_dim], self.batch_dim, aval)
    elif type(self.batch_dim) is RaggedAxis:
      new_aval = core.mapped_aval(
        aval.shape[self.batch_dim.stacked_axis], self.batch_dim.stacked_axis, aval)
      shape = list(new_aval.shape)  # type: ignore
      for ragged_axis, segment_lengths in self.batch_dim.ragged_axes:
        size_tracer = BatchTracer(self._trace, segment_lengths, 0)
        if self.batch_dim.stacked_axis < ragged_axis:
          ragged_axis -= 1
        shape[ragged_axis] = size_tracer
      return core.DShapedArray(shape=tuple(shape), dtype=aval.dtype,
                               weak_type=aval.weak_type)
