def _avals_to_layouts(avals):
  return ir.ArrayAttr.get([_aval_to_layout(a) for a in avals])
