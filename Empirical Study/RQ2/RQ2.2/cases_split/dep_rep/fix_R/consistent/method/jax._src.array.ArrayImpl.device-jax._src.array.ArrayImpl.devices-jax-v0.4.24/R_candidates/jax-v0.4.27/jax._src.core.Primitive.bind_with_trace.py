  def bind_with_trace(self, trace, args, params):
    with pop_level(trace.level):
      out = trace.process_primitive(self, map(trace.full_raise, args), params)
    return map(full_lower, out) if self.multiple_results else full_lower(out)
