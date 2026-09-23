def _unmap_ref(size, axis_name, axis, ref_aval):
  return AbstractRef(core.unmapped_aval(size, axis_name, axis,
                                        ref_aval.inner_aval))
