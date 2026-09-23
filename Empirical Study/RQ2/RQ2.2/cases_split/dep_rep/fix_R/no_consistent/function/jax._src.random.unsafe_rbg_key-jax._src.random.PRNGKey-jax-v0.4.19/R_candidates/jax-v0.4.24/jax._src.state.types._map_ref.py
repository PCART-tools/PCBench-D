def _map_ref(size, axis, ref_aval):
  return AbstractRef(core.mapped_aval(size, axis, ref_aval.inner_aval))
