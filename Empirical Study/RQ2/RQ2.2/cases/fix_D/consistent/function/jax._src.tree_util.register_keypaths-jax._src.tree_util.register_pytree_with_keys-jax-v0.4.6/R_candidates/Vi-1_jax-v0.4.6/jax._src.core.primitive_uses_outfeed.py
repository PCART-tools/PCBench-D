def primitive_uses_outfeed(prim: Primitive, params: Dict) -> bool:
  if prim in outfeed_primitives:
    return True
  for param in params.values():
    if isinstance(param, tuple):
      if any(unsafe_map(_param_uses_outfeed, param)):
        return True
    elif _param_uses_outfeed(param):
      return True
  return False
