def _is_slice_element_none_or_constant(elt):
  """Return True if elt is a constant or None."""
  if elt is None: return True
  try:
    return type(core.get_aval(elt)) is ConcreteArray
  except TypeError:
    return False
