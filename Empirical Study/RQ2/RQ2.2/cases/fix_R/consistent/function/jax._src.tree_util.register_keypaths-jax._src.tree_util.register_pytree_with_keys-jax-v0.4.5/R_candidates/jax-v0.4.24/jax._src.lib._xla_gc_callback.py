def _xla_gc_callback(*args):
  xla_client._xla.collect_garbage()
