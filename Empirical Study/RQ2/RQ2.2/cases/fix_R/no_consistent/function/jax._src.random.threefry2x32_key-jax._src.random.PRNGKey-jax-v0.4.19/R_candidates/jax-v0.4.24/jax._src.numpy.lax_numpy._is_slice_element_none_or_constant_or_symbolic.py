def _is_slice_element_none_or_constant_or_symbolic(elt):
  """Return True if elt is a constant or None."""
  if elt is None: return True
  if core.is_symbolic_dim(elt): return True
  try:
    return type(core.get_aval(elt)) is ConcreteArray
  except TypeError:
    return False
