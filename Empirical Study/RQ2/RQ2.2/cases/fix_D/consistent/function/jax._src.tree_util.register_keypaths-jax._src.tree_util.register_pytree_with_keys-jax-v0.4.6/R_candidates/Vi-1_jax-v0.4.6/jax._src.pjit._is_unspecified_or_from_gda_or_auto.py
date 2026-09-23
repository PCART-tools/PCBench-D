def _is_unspecified_or_from_gda_or_auto(x):
  return _is_from_gda(x) or is_auto(x) or _is_unspecified(x)
