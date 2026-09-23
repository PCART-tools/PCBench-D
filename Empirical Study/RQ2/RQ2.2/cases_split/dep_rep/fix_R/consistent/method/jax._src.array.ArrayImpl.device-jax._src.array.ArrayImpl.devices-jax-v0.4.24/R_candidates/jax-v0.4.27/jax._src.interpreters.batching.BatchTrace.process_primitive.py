  def process_primitive(self, primitive, tracers, params):
    if config.dynamic_shapes.value:
      primitive.abstract_eval(*(t.aval for t in tracers), **params)
    vals_in, dims_in = unzip2((t.val, t.batch_dim) for t in tracers)
    is_axis_primitive = primitive in axis_primitive_batchers
    used_names = core.used_axis_names(primitive, params)
    if is_axis_primitive and _main_trace_for_axis_names(self.main, used_names):
      frame = self.get_frame(vals_in, dims_in)
      batcher_primitive = self.get_axis_primitive_batcher(primitive, frame)
      val_out, dim_out = batcher_primitive(vals_in, dims_in, **params)
    elif all(bdim is not_mapped for bdim in dims_in):
      return primitive.bind(*vals_in, **params)
    else:
      frame = self.get_frame(vals_in, dims_in)
      batched_primitive = self.get_primitive_batcher(primitive, frame)
      val_out, dim_out = batched_primitive(vals_in, dims_in, **params)
    src = source_info_util.current()
    if primitive.multiple_results:
      return [BatchTracer(self, x, d, src) for x, d in zip(val_out, dim_out)]
    else:
      return BatchTracer(self, val_out, dim_out, src)
