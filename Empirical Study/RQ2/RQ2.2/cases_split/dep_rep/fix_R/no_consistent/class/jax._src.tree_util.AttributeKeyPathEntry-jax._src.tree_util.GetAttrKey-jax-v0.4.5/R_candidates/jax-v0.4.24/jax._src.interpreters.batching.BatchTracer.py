class BatchTracer(Tracer):
  __slots__ = ['val', 'batch_dim', 'source_info']

  def __init__(self, trace, val, batch_dim: NotMapped | int | RaggedAxis,
               source_info: source_info_util.SourceInfo | None = None):
    if config.enable_checks.value:
      assert type(batch_dim) in (NotMapped, int, RaggedAxis)
      if type(batch_dim) is int:
        aval = raise_to_shaped(core.get_aval(val))
        assert 0 <= batch_dim < len(aval.shape)  # type: ignore
    self._trace = trace
    self.val = val
    self.batch_dim = batch_dim
    self.source_info = source_info

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

  def full_lower(self):
    if self.batch_dim is not_mapped:
      return core.full_lower(self.val)
    else:
      return self

  def _origin_msg(self):
    if self.source_info is None:
      return ""
    return (f"\nThis BatchTracer with object id {id(self)} was created on line:"
            f"\n  {source_info_util.summarize(self.source_info)}")

  def _contents(self):
    return [('val', self.val), ('batch_dim', self.batch_dim)]

  def get_referent(self):
    if self.batch_dim is None or type(self.batch_dim) is int:
      return core.get_referent(self.val)
    else:  # TODO(mattjj): could handle the RaggedAxis case?
      return self
