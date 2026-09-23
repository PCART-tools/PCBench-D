  def get_axis_primitive_batcher(self, primitive, frame):
    if primitive in spmd_primitive_batchers:
      return partial(spmd_primitive_batchers[primitive],
          frame.size, frame.name, frame.main_trace.trace_type)
    return super().get_axis_primitive_batcher(primitive, frame)
