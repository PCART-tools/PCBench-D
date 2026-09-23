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
