  def sublift(self, tracer):
    return MapTracer(self, tracer.val, tracer.shard_axes)
