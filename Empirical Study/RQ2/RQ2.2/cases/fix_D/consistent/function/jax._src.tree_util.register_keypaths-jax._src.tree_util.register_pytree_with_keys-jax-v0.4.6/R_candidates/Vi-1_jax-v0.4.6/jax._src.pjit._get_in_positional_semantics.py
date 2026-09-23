def _get_in_positional_semantics(arg) -> pxla._PositionalSemantics:
  if isinstance(arg, GDA):
    return pxla._PositionalSemantics.GLOBAL
  return pxla.positional_semantics.val
