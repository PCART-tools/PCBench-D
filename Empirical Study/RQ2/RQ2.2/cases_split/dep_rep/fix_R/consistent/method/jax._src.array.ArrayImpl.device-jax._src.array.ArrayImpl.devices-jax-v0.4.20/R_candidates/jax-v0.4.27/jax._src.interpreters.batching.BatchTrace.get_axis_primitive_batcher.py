  def get_axis_primitive_batcher(self, primitive, frame):
    return partial(axis_primitive_batchers[primitive],
        frame.size, frame.name, frame.main_trace.trace_type)
