  def get_primitive_batcher(self, primitive, frame):
    if primitive in primitive_batchers:
      return primitive_batchers[primitive]
    elif self.spmd_axis_name is not None and primitive in spmd_axis_primitive_batchers:
      return partial(spmd_axis_primitive_batchers[primitive],
                     self.spmd_axis_name, frame.size, frame.name,
                     frame.main_trace.trace_type)
    elif primitive in axis_primitive_batchers:
      return self.get_axis_primitive_batcher(primitive, frame)
    msg = "Batching rule for '{}' not implemented"
    raise NotImplementedError(msg.format(primitive))
