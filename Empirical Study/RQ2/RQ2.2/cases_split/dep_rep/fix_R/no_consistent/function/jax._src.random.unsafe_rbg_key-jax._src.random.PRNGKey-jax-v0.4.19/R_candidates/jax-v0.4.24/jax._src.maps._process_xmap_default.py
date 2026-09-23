def _process_xmap_default(self, call_primitive, f, tracers, params):
  raise NotImplementedError(f"{type(self)} must override process_xmap to handle xmap")
