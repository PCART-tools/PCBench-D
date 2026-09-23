def _ref_raise_to_shaped(ref_aval: AbstractRef, weak_type):
  return AbstractRef(core.raise_to_shaped(ref_aval.inner_aval, weak_type))
