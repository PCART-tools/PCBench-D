  @property
  def aval(self):
    aval = xla.abstractify(self.val)
    shard_axes = dict(self.shard_axes)
    for axis_idx in sorted(shard_axes.values())[::-1]:
      aval = core.mapped_aval(aval.shape[axis_idx], axis_idx, aval)
    return aval
