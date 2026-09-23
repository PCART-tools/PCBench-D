class MapTracer(core.Tracer):
  __slots__ = ["val", "shard_axes"]

  def __init__(self, trace: MapTrace, val, shard_axes: dict[core.AxisName, int]):
    self._trace = trace
    self.val = val
    self.shard_axes = shard_axes
    assert all(val < self.val.ndim for val in self.shard_axes.values())

  @property
  def aval(self):
    aval = xla.abstractify(self.val)
    shard_axes = dict(self.shard_axes)
    for axis_idx in sorted(shard_axes.values())[::-1]:
      aval = core.mapped_aval(aval.shape[axis_idx], axis_idx, aval)
    return aval

  def full_lower(self):
    return self

  def __str__(self):
    named_axes = [f"{k}={v}" for k, v in self.shard_axes.items()]
    return f"{self.val}{{{','.join(named_axes)}}}"
